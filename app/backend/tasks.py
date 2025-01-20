from flask import Blueprint, request, jsonify
import json
from db_management.db_manager import Neo4jManager
from db_management.db_manager import RedisManager
from VulnHunterAI.Vulnhunter.VulnHunterProccess import VulnHunter
#from OnlineSearch.ya_online_search import OnlineSearch
from OnlineSearch.online_search import OnlineSearch
from OnlineSearch.dork_generator import DorkGenerator
from itertools import chain

from celery import Celery
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
celery_route = Celery('backend.tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
neo4j_manager = Neo4jManager()
redis_manager = RedisManager()
celery_bp = Blueprint('celery_bp', __name__)

@celery_route.task(name='backend.tasks.run_scrapy')
def run_scrapy(alias, service, version, urls):
    vulnhunter = VulnHunter()
    vulnhunter.search_and_crawl(alias, service, version, urls)
    return jsonify({"status": "success", "processed_data": f"Procesado el servicio {service} con versión {version}"})

@celery_bp.route('/execute_search_sync', methods=['POST'])
def execute_search_sync():
    data = request.json
    alias = data.get('alias')
    service = data.get('service')
    version = data.get('version')
    neo4j_manager.set_params(alias, service, version)
    neo4j_manager.add_search(alias, service, version)
    keywords = [service, version]
    redis_manager.save_value('project_alias', alias)
    redis_manager.save_value('srv_os', service)
    redis_manager.save_value('version', version)

    with open('/home/user/resources/sites.json', 'r') as file:
        config = json.load(file)
        sites = config['sites']
        sec_domains = config['sec_domains']
        gen_domains = config['general_domains']
    dork_generator = DorkGenerator(sites, sec_domains, gen_domains)
    sec_dorks, gen_dorks = dork_generator.generate_all(keywords)

    # Beta de búsqueda online: REQUIERE DE CONFIGURACIÓN
    online_search = OnlineSearch()
    _, sec_urls, gen_urls = online_search.url_search(sec_dorks, gen_dorks, alias, num_results=100)
    sec_urls = list(chain(*sec_urls))
    gen_urls = list(chain(*gen_urls))
    print(sec_urls)
    
    # URLS para POC de nginx 0.1.5
    #urls = ['https://nvd.nist.gov/vuln/detail/CVE-2009-3896', 'https://nvd.nist.gov/vuln/detail/CVE-2022-44567', "https://nvd.nist.gov/vuln/detail/cve-2017-20005", "https://vulmon.com/vulnerabilitydetails?qid=CVE-2017-20005"]
    
    # Ejecución del crawling
    task = run_scrapy.apply_async(args=[alias, service, version, urls])
    task = run_scrapy.apply_async(args=[alias, service, version, gen_urls])
    
    # Espera el resultado de la tarea de forma síncrona
    while not task.ready():
        pass

    neo4j_manager.update_attributes(alias)
    return jsonify({"status": "success", "processed_data": f"Procesado el servicio {service} con versión {version}", "result": str(task.result)})  # Convertimos el resultado a una cadena
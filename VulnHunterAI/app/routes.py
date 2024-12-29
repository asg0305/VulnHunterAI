from flask import Blueprint, request, jsonify
import subprocess
#from output_config.parse_output import ParseOutput  # Importar la clase ParseOutput
from OnlineSearch.online_search import OnlineSearch
import json
import os
from db_management.db_manager import Neo4jManager

main = Blueprint('main', __name__)

def ejecutar_scrapy():
    """
    spider_name = "sec_spider"
    comando = f'scrapy crawl {spider_name} -a start_urls={search_results}'
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=30)
    print(f'Salida del script:\n{resultado.stdout}')
    if resultado.stderr:
        print(f'Error en el script:\n{resultado.stderr}')
    spider_name = "gen_spider"
    comando = f'scrapy crawl {spider_name} -a start_urls={search_results}'
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=30)
    print(f'Salida del script:\n{resultado.stdout}')
    if resultado.stderr:
        print(f'Error en el script:\n{resultado.stderr}')
    """
    spider_name = "sec_spider"
    comando = f'scrapy crawl {spider_name}'
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    print(f'Salida del script:\n{resultado.stdout}')
    if resultado.stderr:
        print(f'Error en el script:\n{resultado.stderr}')
    spider_name = "gen_spider"
    comando = f'scrapy crawl {spider_name}'
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    print(f'Salida del script:\n{resultado.stdout}')
    if resultado.stderr:
        print(f'Error en el script:\n{resultado.stderr}')

def load_urls_from_jsonl(jsonl_path): 
    urls = [] 
    with open(jsonl_path, 'r') as file: 
        for line in file: 
            data = json.loads(line)
            if 'sec_CVE' in data and 'sec_url' in data: 
                urls.append(data['sec_url']) 
            elif 'gen_CVE' in data and 'gen_url' in data: 
                urls.append(data['gen_url']) 
            elif 'related_CVE' in data and 'related_url' in data: 
                urls.append(data['related_url']) 
    return urls
            
@main.route('/execute_search', methods=['POST'])
def process_data():
    data = request.json
    alias = data.get('alias')
    service = data.get('service')
    version = data.get('version')

    keywords = [service, version]

    with open('/home/user/resources/sites.json', 'r') as file:
        config = json.load(file)
        sites = config['sites']
        sec_domains = config['sec_domains']
        gen_domains = config['general_domains']
    
    # Fase 1: Búsqueda online
    #online_search = OnlineSearch(sites, sec_domains, gen_domains)
    #file_names, sec_search_results, gen_search_results = online_search.google_search(alias, keywords)
    #search_results = sec_search_results, gen_search_results
    #print("Resultados de la búsqueda (General, SecSites y Dominios):")
    #print(search_results)

    # Fase 2: Ejecutar scrapy
    #urls = load_urls_from_jsonl('/home/user/output/Vulnhunter/cve_finder/cve_finder.jsonl')
    #os.chdir("Vulnhunter")
    #results = sec_search_results
    #results.extend(gen_search_results)
    #print(results)
    #ejecutar_scrapy()
    
    return jsonify({"status": "success", "processed_data": f"Procesado el servicio {service} con versión {version}"})


@main.route('/fetch_results', methods=['GET'])
def fetch_results():
    """
    content_filter = request.args.get('content_filter')
    filter_search = request.args.get('filter_search')
    alias = request.args.get('alias')

    # Crear instancia de ParseOutput
    parser = ParseOutput('output_paths')
    alias = "alias"
    # Obtener resultados directamente
    results = parser.parse(alias)

    # Filtrar los resultados
    filtered_results = [result for result in results if content_filter in result['url'] or filter_search in result['search_group'] or alias in result['url']]
    """

    return jsonify({"status": "success"})

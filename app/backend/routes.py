from flask import Blueprint, request, jsonify
import subprocess
import json
import os
from db_management.db_manager import Neo4jManager
from db_management.db_manager import RedisManager
from VulnHunterAI.Vulnhunter.VulnHunterProccess import VulnHunter
from OnlineSearch.online_search import OnlineSearch
from itertools import chain

main = Blueprint('main', __name__)

neo4j_manager = Neo4jManager()
redis_manager = RedisManager()

def ejecutar_scrapy():
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

@main.route('/fetch_results', methods=['GET'])
def fetch_results():

    columns = request.args.get('attributes')
    filters = request.args.get('filters')
    project_alias = redis_manager.get_value('project_alias')
    srv_os = redis_manager.get_value('srv_os')
    version = redis_manager.get_value('version')
    result =  neo4j_manager.get_filtered_results(project_alias, srv_os, version, request_data=columns, filters=filters)
    neo4j_manager.close()

    return jsonify(result)


@main.route('/get_results', methods=['GET'])
def get_results():
    
    columns = request.args.get('attributes')
    project_alias = redis_manager.get_value('project_alias')
    srv_os = redis_manager.get_value('srv_os')
    version = redis_manager.get_value('version')
    result =  neo4j_manager.get_results(project_alias, srv_os, version, request_data=columns)
    neo4j_manager.close()

    return jsonify(result)



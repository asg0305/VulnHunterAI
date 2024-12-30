from flask import Blueprint, request, jsonify
import subprocess
import json
import os
from db_management.db_manager import Neo4jManager

main = Blueprint('main', __name__)
neo4j_manager = Neo4jManager()

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

    os.chdir("Vulnhunter")
    ejecutar_scrapy()
    
    return jsonify({"status": "success", "processed_data": f"Procesado el servicio {service} con versión {version}"})

@main.route('/fetch_results', methods=['GET'])
def fetch_results():
    filters = request.args.to_dict()

    # Extraer parámetros de la petición
    query_type = filters.get('query_type', 'default')
    attribute = filters.get('attribute')
    filter_value = filters.get('filter')
    
    # Asegurarse de que los parámetros no sean None
    if not attribute or not filter_value:
        return jsonify({'error': 'Faltan parámetros attribute o filter'}), 400

    print(attribute)
    print(filter_value)

    # Ejecutar la consulta basada en el tipo de consulta
    if query_type == 'default':
        result = neo4j_manager.get_filtered_default_output(attribute, filter_value)
    elif query_type == 'CVE':
        result = neo4j_manager.get_filtered_CVEs(attribute, filter_value)
    elif query_type == 'exploit':
        result = neo4j_manager.get_filtered_exploits(attribute, filter_value)
    elif query_type == 'related_CVE':
        result = neo4j_manager.get_filtered_related_CVEs(attribute, filter_value)
    elif query_type == 'related_CVE_exploit':
        result = neo4j_manager.get_filtered_related_CVEs_exploits(attribute, filter_value)
    else:
        result = []

    return jsonify(result)


@main.route('/get_results', methods=['GET'])
def get_results():
    query_type = request.args.get('query_type')

    if query_type == 'default':
        result = neo4j_manager.get_default_output()
    elif query_type == 'CVE':
        result = neo4j_manager.get_CVEs()
    elif query_type == 'exploit':
        result = neo4j_manager.get_exploits()
    elif query_type == 'related_CVE':
        result = neo4j_manager.get_related_CVEs()
    elif query_type == 'related_CVE_exploit':
        result = neo4j_manager.get_related_CVEs_exploits()
    else:
        result = []

    return jsonify(result)



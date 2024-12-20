from googlesearch import search
from config.output.output_config import OutputConfig
import json

class OnlineSearch:
    def __init__(self, sites_file):
        # Cargar la lista de sitios y dominios desde el archivo JSON
        with open(sites_file, 'r') as file:
            config = json.load(file)
            self.sites = config['sites']
            self.sec_domains = config['sec_domains']
            self.general_domains = config['general_domains']

    def create_secdomains_query(self, keywords):
        # Crear la consulta de búsqueda por dominio
        keywords_search = ' AND intext:'.join(keywords)
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{domain}" for domain in self.sec_domains])}'
        print(dork_query)
        return dork_query
    
    def create_secsites_dork_query(self, keywords):
        # Crear la consulta de búsqueda utilizando Google Dorks
        keywords_search = ' AND intext:'.join(keywords)
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{site}" for site in self.sites])}'
        print(dork_query)
        return dork_query
    
    def create_generaldomain_query(self, keywords):
        # Crear la consulta de búsqueda por dominio
        keywords_search = ' AND intext:'.join(keywords)
        keywords_search = ' '.join(keywords_search.split(' ') + ['AND intext:', 'exploit', 'AND +intext:','POC'])
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{domain}" for domain in self.general_domains])}'
        print(dork_query)
        return dork_query
    
    def create_general_query(self, keywords):
        # Crear la consulta de búsqueda básica
        keywords_search = ' AND intext:'.join(keywords)
        keywords_search = ' '.join(keywords_search.split(' ') + ['AND intext:', 'vulnerabilities','AND intext:', 'exploit', 'AND +intext:','POC'])
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{domain}" for domain in self.general_domains])}'
        print(dork_query)
        return dork_query
    
    def save_to_file(self, alias, path, content):
        output = OutputConfig(path)
        output.create_json_files(alias, content)

    def google_search(self, alias, keywords, num_results=5):
        # Crear las consultas de búsqueda y obtener resultados de Google
        secdomain_dork_query = self.create_secdomains_query(keywords)
        secsite_dork_query = self.create_secsites_dork_query(keywords)
        generaldomain_dork_query = self.create_generaldomain_query(keywords)
        general_dork_query = self.create_general_query(keywords)

        queries = [secdomain_dork_query, secsite_dork_query, generaldomain_dork_query, general_dork_query]
        search_results = []
        
        for query in queries:
            for result in search(query, num_results):
                if result not in search_results:
                    search_results.append(result)
        
        self.save_to_file(alias, '/home/user/output/OnlineSearch', search_results)

        return search_results

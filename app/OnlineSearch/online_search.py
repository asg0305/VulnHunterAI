from googlesearch import search
from output_config.output_config import OutputConfig

class OnlineSearch:
    def __init__(self, sites, sec_domains, general_domains):
        self.sites = sites
        self.sec_domains = sec_domains
        self.general_domains = general_domains

    def create_secdomains_query(self, keywords):
        # Crear la consulta de búsqueda por dominio
        keywords_search = ' AND intext:'.join(keywords)
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{domain}" for domain in self.sec_domains])}'
        #print(dork_query)
        return dork_query
    
    def create_secsites_dork_query(self, keywords):
        # Crear la consulta de búsqueda utilizando Google Dorks
        keywords_search = ' AND intext:'.join(keywords)
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{site}" for site in self.sites])}'
        #print(dork_query)
        return dork_query
    
    def create_generaldomain_query(self, keywords):
        # Crear la consulta de búsqueda por dominio
        keywords_search = ' AND intext:'.join(keywords)
        keywords_search = ' '.join(keywords_search.split(' ') + ['AND intext:', 'exploit', 'AND +intext:','POC'])
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{domain}" for domain in self.general_domains])}'
        #print(dork_query)
        return dork_query
    
    def create_general_query(self, keywords):
        # Crear la consulta de búsqueda básica
        keywords_search = ' AND intext:'.join(keywords)
        keywords_search = ' '.join(keywords_search.split(' ') + ['AND intext:', 'vulnerabilities','AND intext:', 'exploit', 'AND +intext:','POC'])
        dork_query = f'{"intext:"}{keywords_search}'
        #print(dork_query)
        return dork_query
    
    def save_to_file(self, alias, path, sec_content, gen_content):
        output = OutputConfig(path)
        return output.create_online_search_json_files(alias, sec_content, gen_content)

    def url_search(self, alias, keywords, num_results):
        # Crear las consultas de búsqueda y obtener resultados de Google
        secdomain_dork_query = self.create_secdomains_query(keywords)
        secsite_dork_query = self.create_secsites_dork_query(keywords)
        generaldomain_dork_query = self.create_generaldomain_query(keywords)
        general_dork_query = self.create_general_query(keywords)

        sec_queries = [secdomain_dork_query, secsite_dork_query]
        gen_queries = [generaldomain_dork_query, general_dork_query]
        print(sec_queries)
        sec_search_results = []
        gen_search_results = []
        for query in sec_queries:
            for result in search(query, num_results):
                #print(result)
                if result not in sec_search_results:
                    sec_search_results.append(result)
        
        for query in gen_queries:
            for result in search(query, num_results):
                #print(result)
                if result not in gen_search_results:
                    gen_search_results.append(result)
        
        file_path = self.save_to_file(alias, '/home/user/output/OnlineSearch', sec_search_results, gen_search_results)
        print("Sec")
        print(sec_search_results)

        print("Gen")
        print(gen_search_results)
        return file_path, sec_search_results, gen_search_results

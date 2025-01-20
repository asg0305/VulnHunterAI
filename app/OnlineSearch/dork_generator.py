from output_config.output_config import OutputConfig

class DorkGenerator:

    def __init__(self, sites, sec_domains, general_domains):
        self.sites = sites
        self.sec_domains = sec_domains
        self.general_domains = general_domains
    
    def generate_all(self, keywords):
        sec_queries = []
        gen_queries = []
        sec_queries.append(self.create_secdomains_query(keywords))
        sec_queries.append(self.create_secsites_dork_query(keywords))
        gen_queries.append(self.create_generaldomain_query(keywords))
        gen_queries.append(self.create_general_query(keywords))
        return sec_queries, gen_queries

    def create_secdomains_query(self, keywords):
        keywords_search = ' AND intext:'.join(keywords)
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{domain}" for domain in self.sec_domains])}'
        return dork_query
    
    def create_secsites_dork_query(self, keywords):
        keywords_search = ' AND intext:'.join(keywords)
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{site}" for site in self.sites])}'
        return dork_query
    
    def create_generaldomain_query(self, keywords):
        keywords_search = ' AND intext:'.join(keywords)
        keywords_search = ' '.join(keywords_search.split(' ') + ['AND intext:', 'exploit', 'AND +intext:','POC'])
        dork_query = f'{"intext:"}{keywords_search} {" AND "} {" OR ".join([f"site:{domain}" for domain in self.general_domains])}'
        return dork_query
    
    def create_general_query(self, keywords):
        keywords_search = ' AND intext:'.join(keywords)
        keywords_search = ' '.join(keywords_search.split(' ') + ['AND intext:', 'vulnerabilities','AND intext:', 'exploit', 'AND +intext:','POC'])
        dork_query = f'{"intext:"}{keywords_search}'
        return dork_query

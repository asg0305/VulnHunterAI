from googlesearch import search
from output_config.output_config import OutputConfig

class OnlineSearch:
    def __init__(self):
        pass

    def save_to_file(self, alias, path, sec_content, gen_content):
        output = OutputConfig(path)
        return output.create_online_search_json_files(alias, sec_content, gen_content)
    
    def url_search(self, sec_queries, gen_queries, alias, num_results):
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
        return file_path, sec_search_results, gen_search_results
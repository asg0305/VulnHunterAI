import yagooglesearch
from output_config.output_config import OutputConfig
from .proxies import proxy_list

class OnlineSearch:
    def __init__(self):
        self.proxies = proxy_list

    def search_urls(self, queries, num_results, use_proxies=False):
        results = []
        proxy_rotation_index = 0

        for query in queries:
            if use_proxies:
                proxy_index = proxy_rotation_index % len(self.proxies)

                client = yagooglesearch.SearchClient(
                    query,
                    tbs="li:1",
                    max_search_result_urls_to_return=100,
                    http_429_cool_off_time_in_minutes=45,
                    http_429_cool_off_factor=1.5,
                    verbosity=5,
                    verbose_output=True,
                    proxy=self.proxies[proxy_index]
                )

                if self.proxies[proxy_index].startswith("http://"):
                    client.verify_ssl = False

                client.assign_random_user_agent()
                urls = client.search()

                if "HTTP_429_DETECTED" in urls:
                    print("HTTP 429 detectado... te toca modificar tu búsqueda.")
                    urls.remove("HTTP_429_DETECTED")
                    print("URLs encontradas antes de detectar HTTP 429...")

                proxy_rotation_index += 1
            else:
                client = yagooglesearch.SearchClient(
                    query,
                    tbs="li:1",
                    max_search_result_urls_to_return=num_results,
                    http_429_cool_off_time_in_minutes=45,
                    http_429_cool_off_factor=1.5,
                    verbosity=5,
                    verbose_output=True
                )
                client.assign_random_user_agent()
                urls = client.search()

            results.extend(urls)

        return results
    
    def save_to_file(self, alias, path, sec_content, gen_content):
        output = OutputConfig(path)
        return output.create_online_search_json_files(alias, sec_content, gen_content)
    
    def url_search(self, sec_queries, gen_queries, alias, num_results):
        
        sec_search_results = self.search_urls(sec_queries, num_results, use_proxies=False)
        gen_search_results = self.search_urls(gen_queries, num_results, use_proxies=False)

        file_path = self.save_to_file(alias, '/home/user/output/OnlineSearch', sec_search_results, gen_search_results)
        
        print("Sec")
        print(sec_search_results)

        print("Gen")
        print(gen_search_results)

        return file_path, sec_search_results, gen_search_results


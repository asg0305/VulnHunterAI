import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from OnlineSearch.online_search import OnlineSearch
from Vulnhunter.Vulnhunter.spiders.gen_spider_json import GENSpider
from Vulnhunter.Vulnhunter.spiders.sec_spider import SECSpider
from Vulnhunter.Vulnhunter.spiders.cve_find_spider import CVEFindSpider
from scrapy.settings import Settings
#from Vulnhunter.Vulnhunter.pipelines.temp_pipeline import TempPipeline
import json

class VulnHunter:
    def __init__(self):
        # Obtener el directorio de trabajo actual 
        current_directory = os.getcwd()
        os.chdir("Vulnhunter")
        print("El directorio de trabajo actual es:", current_directory)
        self.settings = get_project_settings()  # Obtener los settings del proyecto Scrapy
        print(self.settings)

    def gen_related_sec_urls(self, related_CVEs):
        related_sec_urls = []
        for CVE in related_CVEs:
            for url in self.sec_domains:
                related_sec_url = url + CVE
                related_sec_urls.append(related_sec_url)
        return related_sec_urls
    
    def search_and_crawl(self, urls):
        #os.chdir("Vulnhunter")
        settings = get_project_settings()
        configure_logging()
        process = CrawlerProcess(settings)
        CVE = "CVE-2023-38408"
        
        current_directory = os.getcwd()
        print("El directorio de trabajo actual es:", current_directory)
        # Ejecutar el primer spider y capturar sus resultados
        process.crawl(CVEFindSpider, start_urls=urls, output_file='/home/user/output/Vulnhunter/cve_finder/alias-2024-12-25-12-14-22.jsonl')
        process.start()  # Elimina la necesidad de reactor.run()
        """
        temp_pipeline = TempPipeline()
        sec_urls = [item['sec_url'] for item in temp_pipeline.items if 'sec_url' in item]
        gen_urls = [item['gen_url'] for item in temp_pipeline.items if 'gen_url' in item]
        related_urls = [item['related_url'] for item in temp_pipeline.items if 'related_url' in item]
        related_CVEs = [item['related_CVE'] for item in temp_pipeline.items if 'related_CVE' in item]

        related_sec_urls = self.gen_related_sec_urls(related_CVEs)

        print("Desde programa")
        final_items = temp_pipeline.get_items()
        print(related_CVEs)
        """
        
        # Ejecutar el segundo spider con los resultados del primero
        #process.crawl(SECSpider, sec_urls=sec_urls, gen_urls=gen_urls, related_urls=related_urls, related_sec_urls=related_sec_urls)
        process.start()  # Elimina la necesidad de reactor.stop()

    def run(self, keywords, urls):
        self.search_and_crawl(urls)

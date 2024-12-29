import os
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from Vulnhunter.Vulnhunter.spiders.gen_spider_json import GENSpider
from Vulnhunter.Vulnhunter.spiders.sec_spider import SECSpider
from Vulnhunter.Vulnhunter.spiders.cve_find_spider import CVEFindSpider
import json

class VulnHunter:
    def __init__(self):
        current_directory = os.getcwd()
        #os.chdir("Vulnhunter")
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

    @defer.inlineCallbacks
    def search_and_crawl(self, urls):
        configure_logging()
        runner = CrawlerRunner(self.settings)
        CVE = "CVE-2023-38408"
        
        #current_directory = os.getcwd()
        #print("El directorio de trabajo actual es:", current_directory)
        
        # Ejecutar el primer spider y capturar sus resultados
        yield runner.crawl(CVEFindSpider)
        """
        # Aquí se puede añadir la lógica para leer el archivo JSONL y procesar los URLs relacionados
        with open('/home/user/output/Vulnhunter/cve_finder/alias-2024-12-25-12-14-22.jsonl', 'r') as file:
            items = [json.loads(line) for line in file]
        
        sec_urls = [item['sec_url'] for item in items if 'sec_url' in item]
        gen_urls = [item['gen_url'] for item in items if 'gen_url' in item]
        related_urls = [item['related_url'] for item in items if 'related_url' in item]
        related_CVEs = [item['related_CVE'] for item in items if 'related_CVE' in item]

        related_sec_urls = self.gen_related_sec_urls(related_CVEs)

        # Ejecutar el segundo spider con los resultados del primero
        yield runner.crawl(SECSpider, start_urls=sec_urls, gen_urls=gen_urls, related_urls=related_urls, related_sec_urls=related_sec_urls)
        """
        reactor.stop()

    def run(self, keywords, urls):
        d = self.search_and_crawl(urls)
        d.addBoth(lambda _: reactor.stop())

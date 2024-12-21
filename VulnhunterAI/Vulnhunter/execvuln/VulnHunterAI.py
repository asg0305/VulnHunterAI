import argparse
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from OnlineSearch.online_search import OnlineSearch
from Vulnhunter.Vulnhunter.spiders.NVD_spider import NVDSpider
from scrapy.settings import Settings
from Vulnhunter.Vulnhunter import settings as my_settings
from Vulnhunter.Vulnhunter.pipelines import JsonWriterPipeline


class VulnHunterAI:
    def __init__(self, sites_file):
        self.online_search = OnlineSearch(sites_file)
        self.results = []
        import os # Obtener el directorio de trabajo actual 
        current_directory = os.getcwd() 
        print("El directorio de trabajo actual es:", current_directory)
        self.settings = get_project_settings()  # Obtener los settings del proyecto Scrapy
        print(self.settings)

    @defer.inlineCallbacks
    def search_and_crawl(self, keywords):
        alias = keywords[0]
        keywords = keywords[1:]
        search_results = self.online_search.google_search(alias, keywords)
        print("Resultados de la búsqueda (General, SecSites y Dominios):")
        print(search_results)
        crawler_settings = Settings()
        
        configure_logging()
        crawler_settings.setmodule(my_settings)
        
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner(crawler_settings)

        yield runner.crawl(NVDSpider, start_urls=search_results, keywords=keywords)
        reactor.stop()

    def run(self, keywords):
        d = self.search_and_crawl(keywords)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VulnHunterAI")
    parser.add_argument("sites_file", help="File containing sites to search")
    parser.add_argument("keywords", help="Keywords to search for")
    
    args = parser.parse_args()

    vuln_hunter = VulnHunterAI(args.sites_file)
    vuln_hunter.run(args.keywords)

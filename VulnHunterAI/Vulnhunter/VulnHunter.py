import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class VulnHunter:
    def __init__(self):
        current_directory = os.getcwd()
        print("El directorio de trabajo actual es:", current_directory)
        self.settings = get_project_settings()  # Obtener los settings del proyecto Scrapy
        print(self.settings)

    def run(self, urls):
        process = CrawlerProcess(self.settings)
        process.crawl('cve_find_spider')
        process.start()  # Maneja automáticamente el ciclo de eventos del reactor

if __name__ == "__main__":
    urls = ['https://example.com']
    hunter = VulnHunter()
    hunter.run(urls)

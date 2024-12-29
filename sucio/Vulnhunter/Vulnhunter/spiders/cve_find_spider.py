from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class CVEFindSpider(CrawlSpider):
    name = "cve_find_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'Vulnhunter.pipelines.duplicates_pipeline.DuplicatesPipeline': 100,
            'Vulnhunter.pipelines.json_pipeline.JsonWriterPipeline': 300,
        }
    }
    def __init__(self, start_urls, output_file, *args, **kwargs):
        super(CVEFindSpider, self).__init__(*args, **kwargs)
        print("cve finder spider")
        self.start_urls = start_urls
        print(self.start_urls)
        print("CVEFINDER PIPELINE FILE")
        print(output_file)

    # Reglas para manejar las URLs y dirigirlas a las funciones de parseo correspondientes
    
    rules = (
        Rule(LinkExtractor(allow=[r"https://nvd.nist.gov/vuln/detail/CVE-.*", 
                                  r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/CVE-.*", 
                                  r"https://vulmon.com/vulnerabilitydetails\?qid=CVE-.*"]), callback="parse_sec"),
        Rule(LinkExtractor(deny=[r"https://nvd.nist.gov/vuln/detail/.*", 
                                  r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/.*", 
                                  r"https://vulmon.com/vulnerabilitydetails\?qid=.*"], 
                            allow=[r".*CVE.*"]), callback="parse_cve"),
        Rule(LinkExtractor(deny=[r"https://nvd.nist.gov/vuln/detail/.*", 
                                 r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/.*", 
                                 r"https://vulmon.com/vulnerabilitydetails\?qid=.*", 
                                 r".*CVE.*"]), callback="parse_content"),
    )
    def parse_sec(self, response):
        print("parse_sec")
        cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
        cve_id = cve_pattern.search(response.url).group() if cve_pattern.search(response.url) else None
        yield {
            "sec_CVE": cve_id,
            "sec_url": response.url
        }

    def parse_cve(self, response):
        print("parse_cve")
        cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
        cve_id = cve_pattern.search(response.url).group() if cve_pattern.search(response.url) else None
        yield {
            "gen_CVE": cve_id,  # Extraer el identificador CVE usando una expresión regular
            "gen_url": response.url  # URL completa que se ha procesado
        }

    def parse_content(self, response):
        print("parse_content")
        cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
        cve_id = cve_pattern.search(response.text).group() if cve_pattern.search(response.text) else None
        yield {
            "related_CVE": cve_id,  # Buscar el identificador CVE en el contenido de la página usando una expresión regular
            "related_url": response.url  # URL completa que se ha procesado
        }

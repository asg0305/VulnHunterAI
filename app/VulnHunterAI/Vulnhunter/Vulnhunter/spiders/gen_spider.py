from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class GENSpider(CrawlSpider):
    name = "gen_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            #"Vulnhunter.pipelines.duplicates_pipeline.DuplicatesPipeline": 100,
            "Vulnhunter.pipelines.db_neo4j_pipeline.Neo4jGeneralPipeline": 200  # Asegúrate de usar el pipeline de Neo4j
        }
    }

    def __init__(self, start_urls=None, *args, **kwargs):
        if start_urls is None:
            start_urls = [
                'https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/cve-2009-3898', 
                'https://nvd.nist.gov/products/cpe/detail/283B2C6C-5991-4C2D-B6C4-0671F3356BDF?namingFormat=2.3&orderBy=CPEURI&keyword=cpe%3A2.3%3Aa%3Af5%3Anginx&status=FINAL%2CDEPRECATED', 
                'https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/cve-2009-3896', 
                'https://vulmon.com/searchpage?q=F5%20Nginx%200.1.0&sortby=byactivity', 
                'https://vulmon.com/searchpage?q=nginx', 
                'https://www.cvedetails.com/version/670629/', 
                'https://www.cvedetails.com/version/1268762/Nginx-NJS-0.1.5.html', 
                'https://www.cvedetails.com/version/1096650/Igor-Sysoev-Nginx-0.1.5.html', 
                'https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/cve-2009-3898', 
                'https://www.incibe.es/incibe-cert/alerta-temprana/vulnerabilidades/cve-2009-3896', 
                'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=image', 
                'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=file+upload', 
                'https://www.csa.gov.sg/alerts-advisories/security-bulletins/2023/sb-2023-002', 
                'https://docs.redhat.com/es/documentation/red_hat_enterprise_linux/8/html-single/8.5_release_notes/index', 
                'https://docs.redhat.com/es/documentation/red_hat_enterprise_linux/8/pdf/8.5_release_notes/red_hat_enterprise_linux-8-8.5_release_notes-en-us.pdf'
            ]
        super(GENSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls

    # Reglas para manejar las URLs y dirigirlas a las funciones de parseo correspondientes
    rules = (
        Rule(LinkExtractor(deny=[r"https://nvd.nist.gov/vuln/detail/.*", 
                                  r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/.*", 
                                  r"https://vulmon.com/vulnerabilitydetails\?qid=.*"], 
                            allow=[r".*CVE.*"]), callback="parse_cve"),
        Rule(LinkExtractor(deny=[r"https://nvd.nist.gov/vuln/detail/.*", 
                                 r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/.*", 
                                 r"https://vulmon.com/vulnerabilitydetails\?qid=.*", 
                                 r".*CVE.*"]), callback="parse_content"),
    )

    def parse_cve(self, response):
        print("parse_cve")
        cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
        cve_id = cve_pattern.search(response.url).group() if cve_pattern.search(response.url) else None
        yield {
            "URL": response.url,  # URL completa que se ha procesado
            "CVE_data": [{
                "CVE": cve_id,
                "url": response.url
            }]
        }

    def parse_content(self, response):
        print("parse_content")
        cve_pattern = re.compile(r"CVE-\d{4}-\d{4,7}")
        cve_id = cve_pattern.search(response.text).group() if cve_pattern.search(response.text) else None
        yield {
            "URL": response.url,  # URL completa que se ha procesado
            "CVE_data": [{
                "CVE": cve_id,
                "url": response.url
            }]
        }

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

class CVEFindSpider(CrawlSpider):
    name = "cve_find_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            "Vulnhunter.pipelines.json_pipeline.CVEFinderPipeline": 100,
            "Vulnhunter.pipelines.duplicates_pipeline.DuplicatesPipeline": 200,
        }
    }
    def __init__(self, file_paths='/home/user/output/OnlineSearch/general-search/alias-gen-2024-12-28-16-10-05.json', *args, **kwargs):
        super(CVEFindSpider, self).__init__(*args, **kwargs)
        print("cve finder spider")
        urls = []
        file_paths = file_paths.split(',')
        print(file_paths)
        for i,file_path in enumerate(file_paths):
            print(self.load_urls_from_json(file_paths[i]))
            urls.extend(self.load_urls_from_json(file_paths[i]))
        self.start_urls = ['https://vulmon.com/vulnerabilitydetails?qid=CVE-2024-3400']
        print("CVEFINDER PIPELINE FILE")

    # Reglas para manejar las URLs y dirigirlas a las funciones de parseo correspondientes
    rules = (
        Rule(LinkExtractor(allow=r"https://nvd.nist.gov/vuln/detail/CVE-.*"), callback="parse_nvd"),
        Rule(LinkExtractor(allow=r"https://vulmon.com/vulnerabilitydetails\?qid=CVE-.*"), callback="parse_vulmon"),
        Rule(LinkExtractor(allow=r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/CVE-.*"), callback="parse_incibe"),
        Rule(LinkExtractor(deny=[r"https://nvd.nist.gov/vuln/detail/.*", 
                                  r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/.*", 
                                  r"https://vulmon.com/vulnerabilitydetails\?qid=.*"], 
                            allow=[r".*CVE.*"]), callback="parse_cve"),
        Rule(LinkExtractor(deny=[r"https://nvd.nist.gov/vuln/detail/.*", 
                                 r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/.*", 
                                 r"https://vulmon.com/vulnerabilitydetails\?qid=.*", 
                                 r".*CVE.*"]), callback="parse_content"),
    )
    
    def parse_nvd(self, response):
        
        exploit_links = response.xpath('//div[@id="vulnHyperlinksPanel"]//table//tr[td[starts-with(@data-testid, "vuln-hyperlinks-resType-")]//span[contains(@class, "badge") and text()="Exploit"]]//td[starts-with(@data-testid, "vuln-hyperlinks-link-")]/a/@href').getall()

        yield {
            "CVE": response.xpath('//span[@data-testid="page-header-vuln-id"]/text()').get(),
            "Description": response.xpath('//p[@data-testid="vuln-description"]/text()').get(),
            "CVSSv3": response.xpath('//*[@id="Cvss3NistCalculatorAnchor"]/text()').get(),
            "Exploit Links": exploit_links,
        }

    def parse_vulmon(self, response):
        
        base_url = "https://vulmon.com"
        exploit_links = response.xpath('//h2[contains(@class, "ui header dividing") and text()="Exploits"]/following-sibling::div[@class="ui divided very relaxed list"]//div[@class="item"]//div[@class="header"]/a/@href').getall()
        full_exploit_links = [urljoin(base_url, link) for link in exploit_links]

        yield {
            "CVE": response.xpath('//div[contains(@class, "ui item")]//div[contains(@class, "content")]//h1[contains(@class, "ui header column jstitle1")]/text()').get().split(' ')[36],
            "Description": response.xpath('//p[contains(@class, "jsdescription1 content_overview")]/text()').get(),
            "CVSSv3": response.xpath('//div[contains(@class, "ui item")]//span[contains(text(), "CVSSv3")]/text()').get().split(': ')[1],
            "Exploit Links": full_exploit_links,
        }

    def parse_incibe(self, response):
        yield {
            "CVE": response.xpath('//h1[contains(@class, "node-title")]/text()').get(),
            "Description": response.xpath('//div[contains(@class, "field-vulnerability-description row") and .//h2[text()="Description"]]//div[contains(@class, "content")]/text()').get(),
            "CVSSv3": response.xpath('//span[@data-testid="vuln-cvssv3-base-score"]/text()').get(),
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

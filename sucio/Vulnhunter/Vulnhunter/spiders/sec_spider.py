from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SECSpider(CrawlSpider):
    name = "sec_spider"
    allowed_domains = ["nvd.nist.gov", "vulmon.com", "www.incibe.es"]

    def __init__(self, output_file, CVE="CVE-2023-38408", *args, **kwargs):
        super(SECSpider, self).__init__(*args, **kwargs)
        print("Sec spider init")
        if CVE:
            print("Sec spider init")
            self.start_urls = [f"https://nvd.nist.gov/vuln/detail/{CVE}", f"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/{CVE}", f"https://vulmon.com/vulnerabilitydetails?qid={CVE}"]
        else:
            self.start_urls = ["https://nvd.nist.gov/", "https://vulmon.com", "https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/"]
        self.output_file = output_file
        self.custom_settings = {
            'ITEM_PIPELINES': {
                'Vulnhunter.pipelines.duplicates_pipeline.DuplicatesPipeline': 100,
                'Vulnhunter.pipelines.json_pipeline.JsonWriterPipeline': 300,
            },
            'OUTPUT_FILE': self.output_file
        }
    
    # PROXY_SERVER = "127.0.0.1"
    # MODIFICAR DOWNLOADER_MIDDLEWARES en settings.py y middlewares.py
    rules = (
        #Rule(LinkExtractor(allow="/vuln/detail/"), callback="parse_nvd"),
        #Rule(LinkExtractor(allow="/vulnerabilitydetails?qid="), callback="parse_vulmon"),
        Rule(LinkExtractor(allow="/incibe-cert/early-warning/vulnerabilities"), callback="parse_incibe"),
    )

    def parse_nvd(self, response):
        print("EJECUTA NVD")
        yield {
            "CVE": response.xpath('//span[@data-testid="page-header-vuln-id"]/text()').get(),
            "Description": response.xpath('//p[@data-testid="vuln-description"]/text()').get(),
            "CVSSv3": response.xpath('//*[@id="Cvss3NistCalculatorAnchor"]/text()').get(),
            "Exploit Links": response.xpath('//div[@id="vulnHyperlinksPanel"]//table//tr[td[starts-with(@data-testid, "vuln-hyperlinks-resType-")]//span[contains(@class, "badge") and text()="Exploit"]]//td[starts-with(@data-testid, "vuln-hyperlinks-link-")]/a/@href').getall(),
        }
    
    def parse_vulmon(self, response):
        print("EJECUTA VULMON")
        base_url = "https://vulmon.com"
        exploit_links = response.xpath('//h2[contains(@class, "ui header dividing") and text()="Exploits"]/following-sibling::div[@class="ui divided very relaxed list"]//div[@class="item"]//div[@class="header"]/a/@href').getall()
        print(exploit_links)
        full_exploit_links = [base_url + link for link in exploit_links]

        yield {
            "CVE": response.xpath('//div[contains(@class, "ui item")]//div[contains(@class, "content")]//h1[contains(@class, "ui header column jstitle1")]/text()').get().split(' ')[36],
            "Description": response.xpath('//p[contains(@class, "jsdescription1 content_overview")]/text()').get(),
            "CVSSv3": response.xpath('//div[contains(@class, "ui item")]//span[contains(text(), "CVSSv3")]/text()').get().split(': ')[1],
            "Exploit Links": full_exploit_links,
        }
    
    def parse_vuln(self, response):
        print("EJECUTA INCIBE")
        cve = response.xpath('//h1[contains(@class, "node-title")]/text()').get()
        print(cve)
        yield {
            "CVE": response.xpath('//h1[contains(@class, "node-title")]/text()').get(),
            "Description": response.xpath('//div[contains(@class, "field-vulnerability-description row") and .//h2[text()="Description"]]//div[contains(@class, "content")]/text()').get(),
            "CVSSv3": response.xpath('//span[@data-testid="vuln-cvssv3-base-score"]/text()').get(),
        }
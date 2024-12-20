from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request

class INCIBESpider(CrawlSpider):
    name = "incibe_crawler"
    allowed_domains = ["www.incibe.es"]

    def __init__(self, CVE="CVE-2023-38408", *args, **kwargs):
        super(INCIBESpider, self).__init__(*args, **kwargs)
        if CVE:
            self.start_urls = [f"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/{CVE}"]
        else:
            self.start_urls = ["https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/"]
    
    # PROXY_SERVER = "127.0.0.1"
    # MODIFICAR DOWNLOADER_MIDDLEWARES en settings.py y middlewares.py
    rules = (
        Rule(LinkExtractor(allow="/en/incibe-cert/early-warning/vulnerabilities/"), callback="parse_vuln"),
    )

    def parse_vuln(self, response):
        yield {
            "CVE": response.xpath('//h1[contains(@class, "node-title")]/text()').get(),
            "Description": response.xpath('//div[contains(@class, "field-vulnerability-description row") and .//h2[text()="Description"]]//div[contains(@class, "content")]/text()').get(),
            "CVSSv3": response.xpath('//span[@data-testid="vuln-cvssv3-base-score"]/text()').get(),
        }

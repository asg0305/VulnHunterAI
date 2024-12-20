from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class NVDSpider(CrawlSpider):
    name = "nvd_crawler"
    allowed_domains = ["nvd.nist.gov"]

    def __init__(self, CVE="CVE-2023-38408", *args, **kwargs):
        super(NVDSpider, self).__init__(*args, **kwargs)
        if CVE:
            self.start_urls = [f"https://nvd.nist.gov/vuln/detail/{CVE}"]
        else:
            self.start_urls = ["https://nvd.nist.gov/"]
    
    # PROXY_SERVER = "127.0.0.1"
    # MODIFICAR DOWNLOADER_MIDDLEWARES en settings.py y middlewares.py
    rules = (
        Rule(LinkExtractor(allow="/vuln/detail/"), callback="parse_vuln"),
    )

    def parse_vuln(self, response):
        yield {
            "CVE": response.xpath('//span[@data-testid="page-header-vuln-id"]/text()').get(),
            "Description": response.xpath('//p[@data-testid="vuln-description"]/text()').get(),
            "CVSSv3": response.xpath('//*[@id="Cvss3NistCalculatorAnchor"]/text()').get(),
            "Exploit Links": response.xpath('//div[@id="vulnHyperlinksPanel"]//table//tr[td[starts-with(@data-testid, "vuln-hyperlinks-resType-")]//span[contains(@class, "badge") and text()="Exploit"]]//td[starts-with(@data-testid, "vuln-hyperlinks-link-")]/a/@href').getall(),
        }

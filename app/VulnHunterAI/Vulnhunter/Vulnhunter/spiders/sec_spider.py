from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin

class SECSpider(CrawlSpider):
    name = "sec_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            "VulnHunterAI.Vulnhunter.Vulnhunter.pipelines.db_neo4j_pipeline.Neo4jSecurePipeline": 200,
        },
        'NEO4J_URI': 'neo4j://neo4j:7687',
        'NEO4J_USER': 'neo4j',
        'NEO4J_PASSWORD': 'password'
    }

    def __init__(self, start_urls, version, *args, **kwargs):
        super(SECSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.version = version
        print(self.start_urls)

    rules = (
        Rule(LinkExtractor(allow=r"https://nvd.nist.gov/vuln/detail/CVE-.*"), callback="parse_nvd"),
        Rule(LinkExtractor(allow=r"https://vulmon.com/vulnerabilitydetails\?qid=CVE-.*"), callback="parse_vulmon"),
        Rule(LinkExtractor(allow=r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/cve-.*"), callback="parse_incibe"),
    )

    def parse_nvd(self, response):
        print(response.url)
        exploit_links = response.xpath('//div[@id="vulnHyperlinksPanel"]//table//tr[td[starts-with(@data-testid, "vuln-hyperlinks-resType-")]//span[contains(@class, "badge") and text()="Exploit"]]//td[starts-with(@data-testid, "vuln-hyperlinks-link-")]/a/@href').getall()

        cve_data = {
            "CVE": response.xpath('//span[@data-testid="page-header-vuln-id"]/text()').get(),
            "description": response.xpath('//p[@data-testid="vuln-description"]/text()').get(),
            "CVSSv3": response.xpath('//*[@id="Cvss3NistCalculatorAnchor"]/text()').get()
        }

        yield {
            "URL": response.url,
            "source": "secure source",
            "CVE_data": [cve_data],
            "Exploit Links": exploit_links,
            "version": self.version
        }

    def parse_vulmon(self, response):
        base_url = "https://vulmon.com"
        exploit_links = response.xpath('//h2[contains(@class, "ui header dividing") and text()="Exploits"]/following-sibling::div[@class="ui divided very relaxed list"]//div[@class="item"]//div[@class="header"]/a/@href').getall()
        full_exploit_links = [urljoin(base_url, link) for link in exploit_links]

        cve_data = {
            "CVE": response.xpath('//div[contains(@class, "ui item")]//div[contains(@class, "content")]//h1[contains(@class, "ui header column jstitle1")]/text()').get().split(' ')[36],
            "description": response.xpath('//p[contains(@class, "jsdescription1 content_overview")]/text()').get(),
            "CVSSv3": response.xpath('//div[contains(@class, "ui item")]//span[contains(text(), "CVSSv3")]/text()').get().split(': ')[1]
        }

        yield {
            "URL": response.url,
            "source": "secure source",
            "CVE_data": [cve_data],
            "Exploit Links": full_exploit_links,
            "version": self.version
        }

    def parse_incibe(self, response):
        cve_data = {
            "CVE": response.xpath('//h1[contains(@class, "node-title")]/text()').get(),
            "description": response.xpath('//div[contains(@class, "field-vulnerability-description row") and .//h2[text()="Description"]]//div[contains(@class, "content")]/text()').get(),
            "CVSSv3": response.xpath('//span[@data-testid="vuln-cvssv3-base-score"]/text()').get()
        }

        yield {
            "URL": response.url,
            "source": "secure source",
            "CVE_data": [cve_data],
            "version": self.version
        }

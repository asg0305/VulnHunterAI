from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urljoin

class SECSpider(CrawlSpider):
    name = "sec_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            #"Vulnhunter.pipelines.duplicates_pipeline.DuplicatesPipeline": 100,
            "Vulnhunter.pipelines.db_neo4j_pipeline.Neo4jSecurePipeline": 200,
        }
    }

    def __init__(self, start_urls=None, *args, **kwargs):
        if start_urls is None:
            start_urls = [
                'https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/cve-2009-3898',
                'https://vulmon.com/vulnerabilitydetails?qid=CVE-2024-3400',
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
        super(SECSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls

    # Reglas para manejar las URLs y dirigirlas a las funciones de parseo correspondientes
    rules = (
        Rule(LinkExtractor(allow=r"https://nvd.nist.gov/vuln/detail/CVE-.*"), callback="parse_nvd"),
        Rule(LinkExtractor(allow=r"https://vulmon.com/vulnerabilitydetails\?qid=CVE-.*"), callback="parse_vulmon"),
        Rule(LinkExtractor(allow=r"https://www.incibe.es/en/incibe-cert/early-warning/vulnerabilities/CVE-.*"), callback="parse_incibe"),
    )
    
    def parse_nvd(self, response):
        print(response.url)
        exploit_links = response.xpath('//div[@id="vulnHyperlinksPanel"]//table//tr[td[starts-with(@data-testid, "vuln-hyperlinks-resType-")]//span[contains(@class, "badge") and text()="Exploit"]]//td[starts-with(@data-testid, "vuln-hyperlinks-link-")]/a/@href').getall()

        cve_data = {
            "CVE": response.xpath('//span[@data-testid="page-header-vuln-id"]/text()').get(),
            "Description": response.xpath('//p[@data-testid="vuln-description"]/text()').get(),
            "CVSSv3": response.xpath('//*[@id="Cvss3NistCalculatorAnchor"]/text()').get()
        }

        yield {
            "URL": response.url,
            "source": "secure source",
            "CVE_data": [cve_data],
            "Exploit Links": exploit_links
        }

    def parse_vulmon(self, response):
        base_url = "https://vulmon.com"
        exploit_links = response.xpath('//h2[contains(@class, "ui header dividing") and text()="Exploits"]/following-sibling::div[@class="ui divided very relaxed list"]//div[@class="item"]//div[@class="header"]/a/@href').getall()
        full_exploit_links = [urljoin(base_url, link) for link in exploit_links]

        cve_data = {
            "CVE": response.xpath('//div[contains(@class, "ui item")]//div[contains(@class, "content")]//h1[contains(@class, "ui header column jstitle1")]/text()').get().split(' ')[36],
            "Description": response.xpath('//p[contains(@class, "jsdescription1 content_overview")]/text()').get(),
            "CVSSv3": response.xpath('//div[contains(@class, "ui item")]//span[contains(text(), "CVSSv3")]/text()').get().split(': ')[1]
        }

        yield {
            "URL": response.url,
            "source": "secure source",
            "CVE_data": [cve_data],
            "Exploit Links": full_exploit_links
        }

    def parse_incibe(self, response):
        cve_data = {
            "CVE": response.xpath('//h1[contains(@class, "node-title")]/text()').get(),
            "Description": response.xpath('//div[contains(@class, "field-vulnerability-description row") and .//h2[text()="Description"]]//div[contains(@class, "content")]/text()').get(),
            "CVSSv3": response.xpath('//span[@data-testid="vuln-cvssv3-base-score"]/text()').get()
        }

        yield {
            "URL": response.url,
            "source": "secure source",
            "CVE_data": [cve_data]
        }

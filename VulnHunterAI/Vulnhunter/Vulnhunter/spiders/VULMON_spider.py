import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
"""
from scrapy.selector import Selector

class VULMONSpider(CrawlSpider):
    name = "vulmon_crawler"
    allowed_domains = ["vulmon.com"]

    def __init__(self, CVE="CVE-2023-38408", *args, **kwargs):
        super(VULMONSpider, self).__init__(*args, **kwargs)
        if CVE:
            self.start_urls = [f"https://vulmon.com/vulnerabilitydetails?qid={CVE}"]
        else:
            self.start_urls = ["https://vulmon.com"]
    
    rules = (
        Rule(LinkExtractor(allow="/vulnerabilitydetails?qid="), callback="parse_vuln"),
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse_vuln_selenium)

    def parse_vuln_selenium(self, response):
        """
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(response.url)

        # Esperar a que el contenido dinámico se cargue
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="content"]'))
        )

        # Obtener el contenido de la página generada dinámicamente
        html = self.driver.page_source
        self.driver.quit()

        # Crear un nuevo selector de Scrapy con el contenido dinámico
        response = Selector(text=html)

        # Llamar a parse_vuln para procesar el contenido
        return self.parse_vuln(response)
        """

    def parse_vuln(self, response):
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

from scrapy.spiders import CrawlSpider

class VULMONSpider(CrawlSpider):
    name = "vulmon_crawler"
    allowed_domains = ["vulmon.com"]

    def __init__(self, CVE="CVE-2023-38408", *args, **kwargs):
        super(VULMONSpider, self).__init__(*args, **kwargs)
        if CVE:
            self.start_urls = [f"https://vulmon.com/vulnerabilitydetails?qid={CVE}"]
        else:
            self.start_urls = ["https://vulmon.com"]

    def parse(self, response):
        base_url = "https://vulmon.com"
        
        exploit_links = response.xpath('//h2[contains(@class, "ui header dividing") and text()="Exploits"]/following-sibling::div[@class="ui divided very relaxed list"]//div[@class="item"]//div[@class="header"]/a/@href').getall()
        print("Exploit Links:", exploit_links)  # Mensaje de depuración

        if not exploit_links:
            print("No se encontraron enlaces de exploits.")  # Mensaje si no se encuentran enlaces
        
        full_exploit_links = [base_url + link for link in exploit_links]

        cve = response.xpath('//div[contains(@class, "ui item")]//div[contains(@class, "content")]//h1[contains(@class, "ui header column jstitle1")]/text()').get()
        if cve:
            cve = cve.strip()
        print("CVE:", cve)  # Mensaje de depuración

        description = response.xpath('//p[contains(@class, "jsdescription1 content_overview")]/text()').get()
        if description:
            description = description.strip()
        print("Description:", description)  # Mensaje de depuración

        cvssv3_text = response.xpath('//div[contains(@class, "ui item")]//span[contains(text(), "CVSSv3")]/text()').get()
        cvssv3 = None
        if cvssv3_text:
            cvssv3 = cvssv3_text.split(': ')[1].strip()
        print("CVSSv3:", cvssv3)  # Mensaje de depuración

        if cve and description and cvssv3 and full_exploit_links:
            yield {
                "CVE": cve,
                "Description": description,
                "CVSSv3": cvssv3,
                "Exploit Links": full_exploit_links,
            }
        else:
            print("No se encontraron todos los elementos necesarios para crear un item.")

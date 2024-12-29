from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class GENSpider(CrawlSpider):
    name = "gen_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'Vulnhunter.pipelines.duplicates_pipeline.DuplicatesPipeline': 100,
            'Vulnhunter.pipelines.json_pipeline.JsonWriterPipeline': 300,
        }
    }

    def __init__(self, output_file, start_urls, *args, **kwargs):
        super(GENSpider, self).__init__(*args, **kwargs)
        print("Gen spider init")
        self.start_urls = start_urls
        self.output_file = output_file
    
    # PROXY_SERVER = "127.0.0.1"
    # MODIFICAR DOWNLOADER_MIDDLEWARES en settings.py y middlewares.py
    rules = (
        Rule(LinkExtractor(allow="/vuln/detail/"), callback="parse"),
    )

    def parse(self, response):
        pass
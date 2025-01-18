from billiard import Process
from scrapy.crawler import CrawlerProcess, Crawler
from scrapy.utils.project import get_project_settings
from VulnHunterAI.Vulnhunter.Vulnhunter.spiders.sec_spider import SECSpider
from scrapy import signals
from twisted.internet import reactor
from twisted.internet.task import deferLater

class UrlCrawlerScript(Process):
    def __init__(self, spider_cls, *args, **kwargs):
        Process.__init__(self)
        self.settings = get_project_settings()
        self.spider_cls = spider_cls
        self.args = args
        self.kwargs = kwargs

    def stop_reactor(self, *args, **kwargs):
        deferLater(reactor, 0, reactor.stop)

    def run(self):
        crawler = Crawler(self.spider_cls, self.settings)
        crawler.signals.connect(self.stop_reactor, signal=signals.spider_closed)
        runner = CrawlerProcess(self.settings)
        runner.crawl(crawler, *self.args, **self.kwargs)
        runner.start()
        reactor.run()

def run_spider(urls, version):
    crawler = UrlCrawlerScript(SECSpider, start_urls=urls, version=version)
    crawler.start()
    crawler.join()

class VulnHunter:
    def __init__(self):
        self.settings = get_project_settings()
    
    def search_and_crawl(self, alias, srv_os, version, urls):
        run_spider(urls, version)
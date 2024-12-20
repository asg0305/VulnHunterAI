import scrapy
#from scrapy_splash import SplashRequest
from scrapy.http import FormRequest
#from bookstore_scraper.items import BookItem  # Asegúrate de tener la clase Item en items.py

class StoreSpider(scrapy.Spider):
    name = 'store_spider'
    login_url = 'http://books.example.com/login'
    start_urls = ['http://books.example.com']

    def start_requests(self):
        yield scrapy.Request(self.login_url, callback=self.parse_login)

    def parse_login(self, response):
        yield FormRequest.from_response(response,
                                        formdata={'username': 'user', 'password': 'pass'},
                                        callback=self.after_login)

    def after_login(self, response):
        if b"authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        else:
            for url in self.start_urls:
                yield SplashRequest(url, callback=self.parse_data, endpoint='execute', args={'lua_source': self.lua_script()})

    def parse_data(self, response):
        for book in response.css('div.book'):
            item = BookItem()
            item['title'] = book.css('h3.title::text').get()
            item['price'] = book.css('p.price::text').get()
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield SplashRequest(response.urljoin(next_page), callback=self.parse_data, endpoint='execute', args={'lua_source': self.lua_script()})

    def lua_script(self):
        return """
        function main(splash)
            splash:set_user_agent(splash.args.ua)
            assert(splash:go(splash.args.url))
            assert(splash:wait(1))
            return {html = splash:html()}
        end
        """

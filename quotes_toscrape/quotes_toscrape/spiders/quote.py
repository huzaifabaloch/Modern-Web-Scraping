# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']

    script = """
        function main(splash, args)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            return splash:html()
        end
    """

    def start_requests(self):
        yield SplashRequest(
            url='http://quotes.toscrape.com',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )

    def parse(self, response):
        for each_quote in response.xpath("//div[@class='quote']"):
            yield {
                'quote': each_quote.xpath(".//span[@class='text']/text()").get(),
                'author': each_quote.xpath(".//span/small/text()").get(),
                'tags': each_quote.xpath(".//div/a/text()").getall()
            }

    
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        absolute_url = response.urljoin(next_page)
        if next_page:
            yield SplashRequest(
                url=absolute_url,
            )
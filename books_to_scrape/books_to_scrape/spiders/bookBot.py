# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookbotSpider(CrawlSpider):
    name = 'bookBot'
    allowed_domains = ['books.toscrape.com']
    #start_urls = ['']
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(
            url='http://books.toscrape.com',
            headers={'User-Agent': self.user_agent}
        )

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), process_request='set_user_agent')
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request


    def parse_item(self, response):
        title = response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get()
        price = response.xpath("(//div[@class='col-sm-6 product_main']/p/text())[1]").get()

        yield {
            'book_name': title,
            'book_price': price,
            #'user_agent': response.request.headers['User-Agent'] 
        }

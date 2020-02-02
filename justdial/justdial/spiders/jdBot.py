# -*- coding: utf-8 -*-
import scrapy   
from ..linkbuilder import link_builder  

class JdbotSpider(scrapy.Spider):
    name = 'jdBot'
    links = link_builder()

    def start_requests(self):
        yield scrapy.Request(
            url=self.links[0],
            callback=self.follow_links
        )

    def follow_links(self, response):
        for link in link_builder():
            yield scrapy.Request(
                url=link,
                callback=self.parse_category,
                dont_filter=True
            )
    
    def parse_category(self, response):
        for c_name in response.xpath("//span[@class='lng_cont_name']/text()"):
            yield {
                'name': c_name.get()
            }

        next_page_link = response.xpath("//a[@rel='next']/@href").get()
        if next_page_link:
            yield scrapy.Request(
                url=next_page_link,
                callback=self.parse_category
            )

    def parse(self, response):
        yield {
            'name': response.xpath("//span[@class='lng_cont_name']/text()").get()
        }

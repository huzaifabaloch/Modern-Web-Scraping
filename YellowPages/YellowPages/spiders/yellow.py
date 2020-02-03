# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class YellowSpider(scrapy.Spider):
    name = 'yellow'
    allowed_domains = ['www.yellowpages.com']
    start_urls = ['https://www.yellowpages.com/search?search_terms=car+Repair+%26+Service&geo_location_terms=San+Francisco%2C+CA']

   

    def parse(self, response):
        for b_name in response.xpath("//div[@class='result']/div/div/div/h2/a"):
            yield {
                'business_url': b_name.xpath(".//@href").get()
            }
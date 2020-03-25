# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from spread_shirt.items import SpreadShirtItem
from scrapy.loader import ItemLoader
import os

class SpreadSpider(scrapy.Spider):
    name = 'spread'

    def start_requests(self):
        urls = ['https://www.spreadshirt.com/custom/products/men-t-shirts-D1CG01',
                'https://www.spreadshirt.com/custom/products/men-hoodies+sweatshirts-D1CG02']

        for url in urls:
            yield SeleniumRequest(
                url=url,
                wait_time=10,
                callback=self.parse
            )

    def parse(self, response):
        
        for each in response.xpath("//div[@class='c-images__picture']"):
            loader = ItemLoader(item=SpreadShirtItem(), selector=each)
            loader.add_xpath('item_name', './/img/@alt')
            rel_url =  each.xpath('.//img/@data-src').get()
            abs_url = response.urljoin(rel_url)
            loader.add_value('image_urls', abs_url.strip())
            yield loader.load_item()

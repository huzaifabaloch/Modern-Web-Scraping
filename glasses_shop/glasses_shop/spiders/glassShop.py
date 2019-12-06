# -*- coding: utf-8 -*-
import scrapy


class GlassshopSpider(scrapy.Spider):
    name = 'glassShop'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        
        for each_block in response.xpath("//div[@class='col-sm-6 col-md-4 m-p-product']"):
            product_url = each_block.xpath(".//div/a/@href").get()
            image_link = each_block.xpath(".//div/a/img/@src").get()
            product_name = each_block.xpath(".//div/p/a/text()").get()
            product_price = each_block.xpath(".//div/div/span/text()").get()
            if product_price:
                if product_price[0] != '$':
                    product_price = each_block.xpath(".//div/div/span/span/text()").get()

            yield {
                'product_url': product_url,
                'image_link': image_link,
                'product_name': product_name,
                'product_price': product_price
            }

        next_page = response.xpath("(//a[@class='page-link'])[1]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

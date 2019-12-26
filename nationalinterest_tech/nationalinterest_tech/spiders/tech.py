# -*- coding: utf-8 -*-
import scrapy


class TechSpider(scrapy.Spider):
    name = 'tech'
    allowed_domains = ['www.nationalinterest.org']
    start_urls = ['https://www.nationalinterest.org/tag/technology']

    def parse(self, response):
        
        for post in response.xpath("//div[@class='article__content']"):
            yield {
                'title': post.xpath(".//h3/a/text()").get(),
                'writer': post.xpath(".//footer/span[@class='meta__author']/a/text()").get(),
                'date_posted': post.xpath(".//footer/span[@class='meta__date']/text()").get()
            }

        next_page = response.xpath("//a[@class='pagination__next']/@href").get()
        if next_page:
            absolute_url = f"https://www.nationalinterest.org{next_page}"
            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse
            )


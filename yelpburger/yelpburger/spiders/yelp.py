# -*- coding: utf-8 -*-
import scrapy


class YelpSpider(scrapy.Spider):
    name = 'yelp'
    # allowed_domains = ['www.yelp.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.yelp.com/search?find_desc=Burgers&find_loc=San+Francisco',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            }
        )

    def parse(self, response):

        for each in response.xpath("//div[@class='lemon--div__373c0__1mboc searchResult__373c0__1yggB border-color--default__373c0__2oFDT']"):
            yield {
                'name': each.xpath(".//h3[@class='lemon--h3__373c0__sQmiG heading--h3__373c0__1n4Of alternate__373c0__1uacp']/span/a/text()").get(),
                'rating': each.xpath(".//div[@class='lemon--div__373c0__1mboc attribute__373c0__1hPI_ display--inline-block__373c0__2de_K u-space-r1 border-color--default__373c0__2oFDT']/span/div/@aria-label").get(),
                'reviews': each.xpath(".//div[@class='lemon--div__373c0__1mboc attribute__373c0__1hPI_ display--inline-block__373c0__2de_K border-color--default__373c0__2oFDT']/span/text()").get(),
                'phone': each.xpath(".//div[@class='lemon--div__373c0__1mboc secondaryAttributes__373c0__7bA0w arrange-unit__373c0__1piwO border-color--default__373c0__2oFDT']/div/div/div/div/p/text()").get(),
                'address': each.xpath(".//div[@class='lemon--div__373c0__1mboc secondaryAttributes__373c0__7bA0w arrange-unit__373c0__1piwO border-color--default__373c0__2oFDT']//address/div/div/div/p/span/text()").get()
            }
              
        next_page = response.xpath("(//div[contains(@class, 'pagination-links')]/div[position() = last()])[2]/a/@href").get()

        #print(next_page)

        if next_page:
            yield response.follow(
                url=next_page,
                callback=self.parse
            )
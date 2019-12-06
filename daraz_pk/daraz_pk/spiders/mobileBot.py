# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class MobilebotSpider(scrapy.Spider):
    name = 'mobileBot'
    allowed_domains = ['www.daraz.pk']

    script = """
        function main(splash, args)
            splash.private_mode_enabled = false
            splash:on_request(function(request)
                request:set_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
            end)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(3))
            --splash:set_viewport_full()
            return splash:html()
        end
    """
    # i used this to get to each extracted url for extracting product name and price.
    script_1 = """
        function main(splash, args)
            splash.private_mode_enabled = false
            splash:on_request(function(request)
                request:set_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
            end)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(3))
            return splash:html()
        end
    """

    def start_requests(self):
        yield SplashRequest(
            url='https://www.daraz.pk/smartphones',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            },
        )

    def parse(self, response):
        # gatherting links from each page.
        for mobile in response.xpath("//div[@class='c3e8SH c2mzns']"):
            link = mobile.xpath("(.//div/div/div/a/@href)[1]").get()[2:]
            link = f'https://{link}'
            #yield {'link': link}

            yield SplashRequest(
                url=link,
                callback=self.parse_mobile,
                endpoint='execute',
                args={
                    'lua_source': self.script_1,
                    'wait': 2,
                },
            )

    def parse_mobile(self, response):
        yield {
            'mobile_name': response.xpath("//span[@class='pdp-mod-product-badge-title']/text()").get(),
            'price': response.xpath("(//div[@class='pdp-product-price']/span/text())[1]").get()
        }
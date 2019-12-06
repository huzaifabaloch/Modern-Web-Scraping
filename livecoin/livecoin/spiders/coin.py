# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.liveocoin.net/en']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(2))
            crypto = splash:select_all('.filterPanelItem___2z5Gb')
            rur_tab = crypto[5]
            rur_tab.mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://www.livecoin.net/en',
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.script
            }
        )


    def parse(self, response):

        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency_pair': currency.xpath('(.//div/div/text())[1]').get(),
                'volume_24h': currency.xpath('(.//div/span/text())[1]').get()
            }

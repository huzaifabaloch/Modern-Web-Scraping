# -*- coding: utf-8 -*-
import scrapy


class SteamSpider(scrapy.Spider):
    name = 'steam'
    allowed_domains = ['store.steampowered.com']
    
    def start_requests(self):
        yield scrapy.Request(
            url='https://store.steampowered.com/search/results?filter=topsellers&page=1&snr=1_7_7_topsellers_7&hide_filtered_results_warning=1',
            callback=self.parse
        )

    def to_html(self, response):
        data = response.body
        with open('raw.html', 'wb') as file:
            file.write(data)

    def parse(self, response):
        for game in response.xpath("//a[@class='search_result_row ds_collapse_flag ']"):
            yield {
                'image_link': game.xpath(".//div[@class='col search_capsule']/img/@src").get(),
                'game_title': game.xpath(".//div[@class='responsive_search_name_combined']/div/span[starts-with(@class, 'title')]/text()").get(),
                'positive_reviews': game.xpath(".//div[@class='responsive_search_name_combined']/div/span[starts-with(@class, 'search')]/@data-tooltip-html").get(),
                'operating_sys': {
                    '1': game.xpath(".//div[@class='responsive_search_name_combined']/div/p/span[contains(@class, 'win')]/@class").get(),
                    '2': game.xpath(".//div[@class='responsive_search_name_combined']/div/p/span[contains(@class, 'mac')]/@class").get(),
                    '3': game.xpath(".//div[@class='responsive_search_name_combined']/div/p/span[contains(@class, 'linux')]/@class").get(),
                },
                'release_date': game.xpath(".//div[@class='responsive_search_name_combined']/div[@class='col search_released responsive_secondrow']/text()").get(), 
                'price': game.xpath("(.//div[@class='responsive_search_name_combined']/div[@class='col search_price_discount_combined responsive_secondrow']/div)[2]/text()").get(),
            }


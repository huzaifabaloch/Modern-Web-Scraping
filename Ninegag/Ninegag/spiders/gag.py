# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.loader import ItemLoader
from Ninegag.items import NinegagItem


class GagSpider(scrapy.Spider):
    name = 'gag'
    start_urls = ['https://9gag.com/v1/group-posts/group/coronavirus/type/hot?after=aL0708v%2CaBgB0bO%2CaGg4gMG&c=10']
    page = 1

    def parse(self, response):
        data = json.loads(response.body)

        for post in data.get('data').get('posts'):
            loader = ItemLoader(item=NinegagItem(), selector=post)
            loader.add_value('title', post.get('title'))
            yield loader.load_item()

        next_cursor = data.get('data').get('nextCursor')

        if next_cursor:
            if self.page <= 10:
                self.page += 1
                next_url = f'https://9gag.com/v1/group-posts/group/coronavirus/type/hot?{next_cursor}'
                yield scrapy.Request(
                    url=next_url,
                    callback=self.parse
                )

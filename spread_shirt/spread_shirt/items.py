# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class SpreadShirtItem(scrapy.Item):
    
    item_name = scrapy.Field(
        output_processor = TakeFirst()
    )

    # These fields should not be called something else when downloading images.
    image_urls = scrapy.Field()
    images = scrapy.Field()

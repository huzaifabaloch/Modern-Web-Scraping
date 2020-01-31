# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class KoncretiItem(scrapy.Item):
    date = scrapy.Field(
        output_processor = TakeFirst()
    )
    month = scrapy.Field(
        output_processor = TakeFirst()
    )
    time = scrapy.Field(
        output_processor = TakeFirst()
    )
    event_title = scrapy.Field(
        output_processor = TakeFirst()
    )
    address_1 = scrapy.Field(
        output_processor = TakeFirst()
    )
    address_2 = scrapy.Field(
        output_processor = TakeFirst()
    )

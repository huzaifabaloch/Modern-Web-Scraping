# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst


class DarazMobilesItem(scrapy.Item):
    mobile_id = scrapy.Field(
        output_processor = TakeFirst()
    )
    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        output_processor = TakeFirst()
    )
    original_price = scrapy.Field(
        output_processor = TakeFirst()
    )
    discount = scrapy.Field(
        output_processor = TakeFirst()
    )
    rating_score = scrapy.Field(
        output_processor = TakeFirst()
    )
    review = scrapy.Field(
        output_processor = TakeFirst()
    )
    url = scrapy.Field(
        output_processor = TakeFirst()
    )
    image_link = scrapy.Field(
        output_processor = TakeFirst()
    )

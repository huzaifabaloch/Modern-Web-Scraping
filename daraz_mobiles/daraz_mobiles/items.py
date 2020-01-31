# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DarazMobilesItem(scrapy.Item):
    mobile_id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    original_price = scrapy.Field()
    discount = scrapy.Field()
    rating_score = scrapy.Field()
    review = scrapy.Field()
    url = scrapy.Field()
    image_link = scrapy.Field()

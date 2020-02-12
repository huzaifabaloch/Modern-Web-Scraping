# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def filter_email(item):
    return item.replace('mailto:', '')

def filter_address(item):
    return item.replace('"', '').replace('"', '')


class YellowpagesItem(scrapy.Item):
    
    business_name = scrapy.Field(
        output_processor = TakeFirst()
    )
    business_address = scrapy.Field(
        input_processor = MapCompose(filter_address),
        output_processor = TakeFirst()
    )
    phone_number = scrapy.Field(
        output_processor = TakeFirst()
    )
    email_address = scrapy.Field(
        input_processor = MapCompose(filter_email),
        output_processor = TakeFirst()
    )
    fax = scrapy.Field(
        output_processor = TakeFirst()
    )
    website = scrapy.Field(
        output_processor = TakeFirst()
    )

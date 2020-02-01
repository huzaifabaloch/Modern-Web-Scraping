# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
import json


def minimum_ticket(price):
    cond = price.get('is_free')
    if bool(cond) == False:
        try:
            return price.get('minimum_ticket_price').get('major_value')
        except AttributeError:
            return None
    else:
        return 'free'

def maximum_ticket(price):
    cond = price.get('is_free')
    if bool(cond) == False:
        try:
            return price.get('maximum_ticket_price').get('major_value') 
        except AttributeError:
            return None 
    else:
        return 'free'

class EventbriteItem(scrapy.Item):
    event_id = scrapy.Field(
        output_processor = TakeFirst()
    )
    event_title = scrapy.Field(
        output_processor = TakeFirst()
    )
    venue = scrapy.Field(
        output_processor = TakeFirst()
    )
    start_date = scrapy.Field(
        output_processor = TakeFirst()
    )
    end_date = scrapy.Field(
        output_processor = TakeFirst()
    )
    start_time = scrapy.Field(
        output_processor = TakeFirst()
    )
    end_time = scrapy.Field(
        output_processor = TakeFirst()
    )
    local_address = scrapy.Field(
        output_processor = TakeFirst()
    )
    longitude = scrapy.Field(
        output_processor = TakeFirst()
    )
    latitude = scrapy.Field(
        output_processor = TakeFirst()
    )
    postal_code = scrapy.Field(
        output_processor = TakeFirst()
    )
    event_ticket_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    minimum_ticket_price = scrapy.Field(
        input_processor = MapCompose(minimum_ticket),
        output_processor = TakeFirst()
    )
    maximum_ticket_price = scrapy.Field(
        input_processor = MapCompose(maximum_ticket),
        output_processor = TakeFirst()
    )

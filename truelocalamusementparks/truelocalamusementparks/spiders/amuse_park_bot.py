# -*- coding: utf-8 -*-
import scrapy
import json

class AmuseParkBotSpider(scrapy.Spider):
    name = 'amuse_park_bot'
    #allowed_domains = ['www.truelocal.com.au']
    
    
    def start_requests(self):
        yield scrapy.Request(
            url='https://api.truelocal.com.au/rest/listings?inventory=true&keyword=amusement-parks&limit=12&offset=0&showCopyPoints=true&type=keyword&location=australia&&passToken=V0MxbDBlV2VNUw==',
            callback=self.parse
        )

    def create_json(self, response):
        data = json.loads(response.body)
        with open('amusement_parks.json', 'w') as file:
            file.write(json.dumps(data))

    def parse(self, response):
        true_data = json.loads(response.body)

        for each in true_data.get('data').get('listing'):
            yield {
                'name': each.get('name'),
                'state': each.get('addresses').get('address')[0].get('state'),
                'latitude': each.get('addresses').get('address')[0].get('latitude'),
                'longitude': each.get('addresses').get('address')[0].get('longitude'),
                'postal_code': each.get('addresses').get('address')[0].get('postCode'),
                'slogan': each.get('slogan'),
                'description': each.get('description'),
            }

        next_page = true_data.get('data')
        offset = next_page.get('offset')
        limit = next_page.get('limit')
        offset += limit  

        yield scrapy.Request(
            url=f'https://api.truelocal.com.au/rest/listings?inventory=true&keyword=amusement-parks&limit={limit}&offset={offset}&showCopyPoints=true&type=keyword&location=australia&&passToken=V0MxbDBlV2VNUw=='
        )



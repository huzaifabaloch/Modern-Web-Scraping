import scrapy 
from scrapy.loader import ItemLoader
import json
from ..items import DarazMobilesItem

class DarazSpider(scrapy.Spider):
    name = 'darazBot'
    allowed_domains = ['www.daraz.pk']
    page = 1
    result_count = 0

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.daraz.pk/smartphones/?ajax=true&page=1',
            callback=self.parse
        )

    def raw_data(self, response):
        data = json.loads(response.body)
        with open('raw_data.json', 'w') as file:
            file.write(json.dumps(data))

    def parse(self, response):
        data = json.loads(response.body)
        mobileItem = DarazMobilesItem()

        mobiles_listing = data.get('mods').get('listItems')
        for each_listing in mobiles_listing:
            loader = ItemLoader(item=DarazMobilesItem())
            loader.add_value('mobile_id', each_listing.get('nid'))
            loader.add_value('name', each_listing.get('name'))
            loader.add_value('price', each_listing.get('price'))
            loader.add_value('original_price', each_listing.get('originalPrice'))
            loader.add_value('discount', each_listing.get('discount'))
            loader.add_value('rating_score', each_listing.get('ratingScore'))
            loader.add_value('review', each_listing.get('review'))
            loader.add_value('url', each_listing.get('productUrl'))
            loader.add_value('image_link', each_listing.get('image'))
            self.result_count += 1

            yield loader.load_item()
        
        total_results = data.get('mainInfo').get('totalResults')
        if self.result_count <= int(total_results):
            self.page += 1
            nxt_url = f'https://www.daraz.pk/smartphones/?ajax=true&page={self.page}'
            yield scrapy.Request(
                url=nxt_url,
                callback=self.parse
            )

# -*- coding: utf-8 -*-
import scrapy
import json

class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['www.zillow.com']
    request = 1

    def start_requests(self):
        yield scrapy.Request(
                url='https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A1%7D%2C%22usersSearchTerm%22%3A%22Miami%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.45882581640626%2C%22east%22%3A-80.03585218359376%2C%22south%22%3A25.609314017670446%2C%22north%22%3A25.935798428223915%7D%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=false&includeList=true',
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
            },
            callback=self.parse
        )

    def to_json(self, response):
        data = json.loads(response.body)
        with open('raw_data.json', 'w') as file:
            file.write(json.dumps(data))

    def parse(self, response):
        miami_data = json.loads(response.body)

        search_results = miami_data.get('searchResults').get('listResults')
        for estate in search_results:
            yield {
                'address': estate.get('address'),
                'addressState': estate.get('addressState'),
                'beds': estate.get('beds'),
                'baths': estate.get('baths'),
                'area': estate.get('area'),
                'brokerName': estate.get('brokerName'),
                'brokerPhone': estate.get('brokerPhone'),
                'latitude': estate.get('latLong').get('latitude'),
                'longitude': estate.get('latLong').get('longitude'),
            }

        if self.request != 1:
            current_page = miami_data.get('queryState').get('pagination').get('currentPage')
            total_page = miami_data.get('searchList').get('totalPages')
            next_page = current_page + 1
        else:
            current_page = miami_data.get('defaultQueryState').get('pagination').get('currentPage')
            total_page = miami_data.get('searchList').get('totalPages')
            next_page = current_page + 1
            self.request += 1

        if next_page <= total_page:
            yield scrapy.Request(
                url='https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A{}%7D%2C%22usersSearchTerm%22%3A%22Miami%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-80.45882581640626%2C%22east%22%3A-80.03585218359376%2C%22south%22%3A25.609314017670446%2C%22north%22%3A25.935798428223894%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22mapZoom%22%3A11%2C%22filterState%22%3A%7B%7D%2C%22isListVisible%22%3Atrue%7D&includeMap=false&includeList=true'.format(str(next_page)),
                callback=self.parse,
                headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
            }
            )

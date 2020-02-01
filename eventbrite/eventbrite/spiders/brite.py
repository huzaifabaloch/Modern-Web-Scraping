# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import EventbriteItem
import json

class BriteSpider(scrapy.Spider):
    name = 'brite'
    allowed_domains = ['www.eventbrite.com']

    payload = "{\n    \"event_search\": {\n        \"dates\": \"current_future\",\n        \"places\": [\n            \"85922583\"\n        ],\n        \"page\": 1,\n        \"page_size\": 20,\n        \"online_events_only\": false\n    },\n    \"expand.destination_event\": [\n        \"primary_venue\",\n        \"image\",\n        \"ticket_availability\",\n        \"saves\",\n        \"series\",\n        \"my_collections\",\n        \"event_sales_status\"\n    ]\n}"
    page_number = 1

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.eventbrite.com/api/v3/destination/search",
            callback=self.parse,
            method="POST",
            body=self.payload,
            headers={
                "Cookie": "mgrefby=; G=v%3D2%26i%3D04a6a593-b419-451f-9ac7-8912a963e9b4%26a%3Dc6c%26s%3Dd5758d1aa25c0cfb0796627ab2a0d2e3b3e89548; ebEventToTrack=; eblang=lo%3Den_US%26la%3Den-us; AN=; mgref=typeins; csrftoken=dbb779f036e411eab665ef1f6bf713f4; _ga=GA1.2.687545818.1579016719; ebGAClientId=687545818.1579016719; _gaexp=GAX1.2.VMDdMrAiSGGJcy4TVI4fsA.18364.1; mgaff55392014005=ebdssbdestsearch; mgref=eafil; _gcl_au=1.1.440292761.1579025793; _fbp=fb.1.1579025797117.1453060398; mgaff55392014005=ebdssbdestsearch; mgaff62042651240=ebdssbdestsearch; mgaff62042651240=ebdssbdestsearch; _gid=GA1.2.1416921008.1580542895; cm=%5B55392014005%2C%2062042651240%2C%2059806133756%5D; mgaff59806133756=ebdssbdestsearch; location=%7B%22place_id%22%3A%20%2285675757%22%2C%20%22place_type%22%3A%20%22region%22%2C%20%22current_place_parent%22%3A%20%22Pakistan%22%2C%20%22longitude%22%3A%2067.0817%2C%20%22current_place%22%3A%20%22Sind%22%2C%20%22latitude%22%3A%2024.9043%2C%20%22slug%22%3A%20%22pakistan--sind%22%7D; SS=AE3DLHRMonqf1Y5SxXNP8VLKQSxG3STy9g; AS=fe745e52-2735-41a3-9e48-a01e980a9514; SERVERID=djc36; lux_uid=158057289478020711; location={%22slug%22:%22ca--san-francisco%22%2C%22place_id%22:%2285922583%22%2C%22latitude%22:37.7749295%2C%22longitude%22:-122.4194155%2C%22place_type%22:%22locality%22%2C%22current_place%22:%22San%20Francisco%22%2C%22current_place_parent%22:%22CA%2C%20USA%22%2C%22is_online%22:false}; SP=AGQgbbnCBwKQwod6KVsMja76aA8jSzNz1D-WQyWZicPpKcFJ7V9t35lqIq-ITZ6xxMk7sEKzgyA6A-geEtgXyqtdKk7sf4SEMTz-IzDTBJ4gTibIdA9AKrkBnWsCzs5rvVzaGHwvwZwqkxvELeAoIyUGQg2LsMMFsbgyI1RsRftQQGp4IW5MW7Gqsc55uwDOCMmQjgzqqlJJ1pWBX6Z4A0eXeW-m0H5htOXP5z69FHSEahU8KBMuIT8; janus=v%3D1%26exp_eb_127335_derank_sold_out_events_in_search%3DNone%26exp_eb_search_experiment_3%3DNone%26exp_eb_search_experiment_4%3DNone; _gat=1",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                "X-CSRFToken": "dbb779f036e411eab665ef1f6bf713f4",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://www.eventbrite.com/api/v3/destination/search/log_requests"
            }
        )

    def payload_modify(self):
        self.payload = "{\n    \"event_search\": {\n        \"dates\": \"current_future\",\n        \"places\": [\n            \"85922583\"\n        ],\n        \"page\": %d,\n        \"page_size\": 20,\n        \"online_events_only\": false\n    },\n    \"expand.destination_event\": [\n        \"primary_venue\",\n        \"image\",\n        \"ticket_availability\",\n        \"saves\",\n        \"series\",\n        \"my_collections\",\n        \"event_sales_status\"\n    ]\n}"%(self.page_number)

    def raw_data(self, response):
        data = json.loads(response.body)
        with open('raw_data.json', 'w') as file:
            file.write(json.dumps(data))

    def parse(self, response):
        data = json.loads(response.body)
        events = data.get('events').get('results')
        for event in events:
            loader = ItemLoader(item=EventbriteItem())
            loader.add_value('event_id', event.get('eventbrite_event_id'))
            loader.add_value('event_title', event.get('name'))
            loader.add_value('minimum_ticket_price', event.get('ticket_availability'))
            loader.add_value('maximum_ticket_price', event.get('ticket_availability'))
            #print(event.get('ticket_availability'))
            loader.add_value('venue', event.get('primary_venue').get('name'))
            loader.add_value('start_date', event.get('start_date'))
            loader.add_value('end_date', event.get('end_date'))
            loader.add_value('start_time', event.get('start_time'))
            loader.add_value('end_time', event.get('end_time'))
            loader.add_value('local_address', event.get('primary_venue').get('address').get('localized_address_display'))
            loader.add_value('longitude', event.get('primary_venue').get('address').get('longitude'))
            loader.add_value('latitude', event.get('primary_venue').get('address').get('latitude'))
            loader.add_value('postal_code', event.get('primary_venue').get('address').get('postal_code'))
            loader.add_value('event_ticket_url', event.get('tickets_url'))
            try:
                loader.add_value('image_url', event.get('image').get('url'))
            except:
                loader.add_value('image_url', None)

            yield loader.load_item()

        page_count = data.get('events').get('pagination').get('page_count')

        if self.page_number <= page_count:
            self.page_number += 1
            self.payload_modify()
            yield scrapy.Request(
                url="https://www.eventbrite.com/api/v3/destination/search",
                callback=self.parse,
                method="POST",
                body=self.payload,
                headers={
                    "Cookie": "mgrefby=; G=v%3D2%26i%3D04a6a593-b419-451f-9ac7-8912a963e9b4%26a%3Dc6c%26s%3Dd5758d1aa25c0cfb0796627ab2a0d2e3b3e89548; ebEventToTrack=; eblang=lo%3Den_US%26la%3Den-us; AN=; mgref=typeins; csrftoken=dbb779f036e411eab665ef1f6bf713f4; _ga=GA1.2.687545818.1579016719; ebGAClientId=687545818.1579016719; _gaexp=GAX1.2.VMDdMrAiSGGJcy4TVI4fsA.18364.1; mgaff55392014005=ebdssbdestsearch; mgref=eafil; _gcl_au=1.1.440292761.1579025793; _fbp=fb.1.1579025797117.1453060398; mgaff55392014005=ebdssbdestsearch; mgaff62042651240=ebdssbdestsearch; mgaff62042651240=ebdssbdestsearch; _gid=GA1.2.1416921008.1580542895; cm=%5B55392014005%2C%2062042651240%2C%2059806133756%5D; mgaff59806133756=ebdssbdestsearch; location=%7B%22place_id%22%3A%20%2285675757%22%2C%20%22place_type%22%3A%20%22region%22%2C%20%22current_place_parent%22%3A%20%22Pakistan%22%2C%20%22longitude%22%3A%2067.0817%2C%20%22current_place%22%3A%20%22Sind%22%2C%20%22latitude%22%3A%2024.9043%2C%20%22slug%22%3A%20%22pakistan--sind%22%7D; SS=AE3DLHRMonqf1Y5SxXNP8VLKQSxG3STy9g; AS=fe745e52-2735-41a3-9e48-a01e980a9514; SERVERID=djc36; lux_uid=158057289478020711; location={%22slug%22:%22ca--san-francisco%22%2C%22place_id%22:%2285922583%22%2C%22latitude%22:37.7749295%2C%22longitude%22:-122.4194155%2C%22place_type%22:%22locality%22%2C%22current_place%22:%22San%20Francisco%22%2C%22current_place_parent%22:%22CA%2C%20USA%22%2C%22is_online%22:false}; SP=AGQgbbnCBwKQwod6KVsMja76aA8jSzNz1D-WQyWZicPpKcFJ7V9t35lqIq-ITZ6xxMk7sEKzgyA6A-geEtgXyqtdKk7sf4SEMTz-IzDTBJ4gTibIdA9AKrkBnWsCzs5rvVzaGHwvwZwqkxvELeAoIyUGQg2LsMMFsbgyI1RsRftQQGp4IW5MW7Gqsc55uwDOCMmQjgzqqlJJ1pWBX6Z4A0eXeW-m0H5htOXP5z69FHSEahU8KBMuIT8; janus=v%3D1%26exp_eb_127335_derank_sold_out_events_in_search%3DNone%26exp_eb_search_experiment_3%3DNone%26exp_eb_search_experiment_4%3DNone; _gat=1",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
                    "X-CSRFToken": "dbb779f036e411eab665ef1f6bf713f4",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": "https://www.eventbrite.com/api/v3/destination/search/log_requests"
                }
            )


        

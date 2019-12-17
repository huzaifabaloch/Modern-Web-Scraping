# -*- coding: utf-8 -*-
import scrapy
import json

class AirbnbbotSpider(scrapy.Spider):
    name = 'airbnbBot'
    allowed_domains = ['www.airbnb.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=05b7ba0f-9d62-446c-acce-b9a756d8e1b6&currency=USD&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&map_toggle=false&metadata_only=false&query=New%20York%20%C2%B7%20Stays&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.2.3&screen_height=663&screen_size=large&screen_width=1366&search_type=search_query&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=300&version=1.7.0',
            callback=self.parse
        )

    def parse_id(self, response):
        data = json.loads(response.body)
        with open('stays.json', 'w') as file: 
            file.write(json.dumps(data))

    def parse(self, response):
        data = json.loads(response.body)

        try:
            stays = data.get('explore_tabs')[0].get('sections')[2].get('listings')

        except IndexError:
            stays = data.get('explore_tabs')[0].get('sections')[0].get('listings')


        print('\n\n')
        for i in stays:
            yield {
                'id': i.get('listing').get('id'),
                'name': i.get('listing').get('name'),
                'no_of_bedroom': i.get('listing').get('bedrooms'),
                'no_of_bathroom': i.get('listing').get('bathrooms'),
                'guest_label': i.get('listing').get('guest_label'),
                'latitude': i.get('listing').get('lat'),
                'longitude': i.get('listing').get('lng'),
                'person_capacity': i.get('listing').get('person_capacity'),
            }

        
        pagination_meta_data = data.get('explore_tabs')[0].get('pagination_metadata')


        if pagination_meta_data.get('has_next_page'):
            item_offsets = pagination_meta_data.get('items_offset') 
            section_offset = pagination_meta_data.get('section_offset')
            yield scrapy.Request(
                url='https://www.airbnb.com/api/v2/explore_tabs?_format=for_explore_search_web&auto_ib=true&client_session_id=05b7ba0f-9d62-446c-acce-b9a756d8e1b6&currency=USD&current_tab_id=home_tab&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&hide_dates_and_guests_filters=false&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_per_grid=18&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=en&map_toggle=false&metadata_only=false&query=New%20York%20%C2%B7%20Stays&query_understanding_enabled=true&refinement_paths%5B%5D=%2Fhomes&satori_version=1.2.3&screen_height=663&screen_size=large&screen_width=1366&search_type=search_query&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=300&version=1.7.0&items_offset={0}&section_offset={1}&'.format(item_offsets, section_offset),
                callback=self.parse
            ) 


        print('\n\n')
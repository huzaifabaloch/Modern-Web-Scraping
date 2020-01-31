# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
import json
from ..items import KoncretiItem

class KoncretiSpider(scrapy.Spider):
    name = 'koncreti'
    start_urls = ['https://www.filharmonija.si/koncerti']
    page = 0

    def parse(self, response):
        yield FormRequest.from_response(response=response, method="POST", url="https://www.filharmonija.si/wp-admin/admin-ajax.php", formdata={
            "action": "the_ajax_hook",
            "direction": "next",
            "shortcode[hide_past]": "no",
            "shortcode[show_et_ft_img]": "yes",
            "shortcode[event_order]": "ASC",
            "shortcode[ft_event_priority]": "no",
            "shortcode[lang]": "L1",
            "shortcode[month_incre]": "0",
            "shortcode[only_ft]": "no",
            "shortcode[evc_open]": "no",
            "shortcode[show_limit]": "no",
            "shortcode[etc_override]": "no",
            "shortcode[show_limit_redir]": "0",
            "shortcode[tiles]": "no",
            "shortcode[tile_height]": "0",
            "shortcode[tile_bg]": "0",
            "shortcode[tile_count]": "2",
            "shortcode[tile_style]": "0",
            "shortcode[members_only]": "no",
            "shortcode[ux_val]": "0",
            "shortcode[show_limit_ajax]": "no",
            "shortcode[show_limit_paged]": "1",
            "shortcode[hide_mult_occur]": "no",
            "shortcode[show_repeats]": "no",
            "shortcode[sep_month]": "no",
            "shortcode[number_of_months]": "1",
            "evodata[cyear]": "2020",
            "evodata[cmonth]": "0",
            "evodata[runajax]": "1",
            "evodata[evc_open]": "0",
            "evodata[cal_ver]": "2.6.8",
            "evodata[mapscroll]": "true",
            "evodata[mapformat]": "roadmap",
            "evodata[mapzoom]": "18",
            "evodata[ev_cnt]": "0",
            "evodata[show_limit]": "no",
            "evodata[tiles]": "no",
            "evodata[sort_by]": "sort_date",
            "evodata[filters_on]": "false",
            "evodata[range_start]": "0",
            "evodata[range_end]": "0",
            "evodata[send_unix]": "0",
            "evodata[ux_val]": "0",
            "evodata[accord]": "0",
            "evodata[rtl]": "no",
            "ajaxtype": "switchmonth"
        }, 
        headers={
            "Cookie": "MAILPOET_SESSION=%22a3og876p04ookw0wsg448s0gg4c4oswo%22; PHPSESSID=kk0k5el7tpjbmvajpompkb686n",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }, callback=self.response_data)


    def response_data(self, response):
        data = json.loads(response.body)

        total_events = data.get('total_events')
        if total_events:
            content = data.get('content')
            resp = Selector(text=content)
            for each_resp in resp.xpath("//div[contains(@class, 'eventon_list_event evo_eventtop')]"):
                loader = ItemLoader(item=KoncretiItem(), selector=each_resp, response=response)
                loader.add_xpath('date', ".//p/a/span/span/em[@class='date']/text()")
                loader.add_xpath('month', ".//p/a/span/span/em[@class='month']/text()")
                loader.add_xpath('time', ".//p/a/span/span/em[@class='time']/text()")
                loader.add_xpath('event_title', ".//p/a/span/span[@class='evcal_desc2 evcal_event_title']/text()")

                yield loader.load_item()

            month = data.get('month')
            year = data.get('year')
            self.page = self.page + 1

            if month:
                yield scrapy.Request(   
                    url="http://quotes.toscrape.com/login",
                    callback=self.next_response,
                    meta={
                        'month': month,
                        'year': year
                    },
                    dont_filter=True
                )
  
    def next_response(self, response):
        month = response.meta['month']
        year = response.meta['year']

        yield FormRequest.from_response(response=response, method="POST", url="https://www.filharmonija.si/wp-admin/admin-ajax.php", formdata={
            "action": "the_ajax_hook",
            "direction": "next",
            "shortcode[hide_past]": "no",
            "shortcode[show_et_ft_img]": "yes",
            "shortcode[event_order]": "ASC",
            "shortcode[ft_event_priority]": "no",
            "shortcode[lang]": "L1",
            "shortcode[month_incre]": "0",
            "shortcode[only_ft]": "no",
            "shortcode[evc_open]": "no",
            "shortcode[show_limit]": "no",
            "shortcode[etc_override]": "no",
            "shortcode[show_limit_redir]": "0",
            "shortcode[tiles]": "no",
            "shortcode[tile_height]": "0",
            "shortcode[tile_bg]": "0",
            "shortcode[tile_count]": "2",
            "shortcode[tile_style]": "0",
            "shortcode[members_only]": "no",
            "shortcode[ux_val]": "0",
            "shortcode[show_limit_ajax]": "no",
            "shortcode[show_limit_paged]": "1",
            "shortcode[hide_mult_occur]": "no",
            "shortcode[show_repeats]": "no",
            "shortcode[sep_month]": "no",
            "shortcode[number_of_months]": "1",
            "evodata[cyear]": str(year),
            "evodata[cmonth]": str(month),
            "evodata[runajax]": "1",
            "evodata[evc_open]": "0",
            "evodata[cal_ver]": "2.6.8",
            "evodata[mapscroll]": "true",
            "evodata[mapformat]": "roadmap",
            "evodata[mapzoom]": "18",
            "evodata[ev_cnt]": "0",
            "evodata[show_limit]": "no",
            "evodata[tiles]": "no",
            "evodata[sort_by]": "sort_date",
            "evodata[filters_on]": "false",
            "evodata[range_start]": "0",
            "evodata[range_end]": "0",
            "evodata[send_unix]": "0",
            "evodata[ux_val]": "0",
            "evodata[accord]": "0",
            "evodata[rtl]": "no",
            "ajaxtype": "switchmonth"
        }, headers={
            "Cookie": "MAILPOET_SESSION=%22a3og876p04ookw0wsg448s0gg4c4oswo%22; PHPSESSID=kk0k5el7tpjbmvajpompkb686n",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }, callback=self.response_data)
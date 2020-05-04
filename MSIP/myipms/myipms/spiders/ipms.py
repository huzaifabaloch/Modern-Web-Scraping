# -*- coding: utf-8 -*-
import scrapy
import json


class IpmsSpider(scrapy.Spider):
    name = 'ipms'
    payload = '{\\"getpage": "yes", "lang": "en"}'

    headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '19',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 's2_csrf_cookie_name=3c111c8c0e52355f4fad0f2723d1ed3d; PHPSESSID=k215kcd51cbpruhkkp66krqie6; sw=134.9; sh=66.3; _ga=GA1.2.797439241.1588021291; _gid=GA1.2.215352006.1588021291; __gads=ID=6030cdad3da56a15:T=1588021296:S=ALNI_MYHF2Zdj8vwDzyDcBxeBrzT6uLFMQ; s2_uGoo=33af47f79b546d159e0bb11b5de9d24a947f2abd; s2_csrf_cookie_name=3c111c8c0e52355f4fad0f2723d1ed3d; _gat=1; __unam=737437c-171bd71e950-2dd2390f-12',
    'Host': 'myip.ms',
    'Origin': 'https://myip.ms',
    'Referer': 'https://myip.ms/browse/sites/1/own/376714/sort/6',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
    }

    def start_requests(self):
        yield scrapy.Request(
            url='https://myip.ms/ajax_table/sites/1/own/376714/sort/6',
            method='POST',
            body=self.payload,
            headers=self.headers,
            callback=self.parse
        )

    def parse(self, response):
        print(response.body)

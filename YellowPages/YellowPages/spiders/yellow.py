# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import YellowpagesItem


class YellowSpider(scrapy.Spider):
    name = 'repair_service'
    allowed_domains = ['www.yellowpages.com']

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.yellowpages.com/search?search_terms=car+Repair+%26+Service&geo_location_terms=San+Francisco%2C+CA',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
                'Cookie': 'vrid=10201013-fcc3-4a62-87bf-ef713134719c; s_ecid=MCMID%7C41080614554986137501106057387303695903; _ga=GA1.2.449137245.1573220384; _fbp=fb.1.1573220385131.1235717397; s_prop70=November; s_prop71=45; __gads=ID=b6ec4a1936b0eb13:T=1573220469:S=ALNI_MZ3ZC801AzROOv3OIrSH5_gdIWZkA; search_terms=car%20Repair%20%26%20Service; _gid=GA1.2.879932352.1580749332; location=geo_term%3ASan%20Francisco%2C%20CA%7Clat%3A37.7749295%7Clng%3A-122.4194155%7Ccity%3ASan%20Francisco%7Cstate%3ACA%7Cdisplay_geo%3ASan%20Francisco%2C%20CA; express:sess=eyJka3MiOiI5ZjRjZTE4YS0yYWIxLTRjNDUtOWIxZi04Yzk3ODIwMDkxYWUiLCJmbGFzaCI6e30sInByZXZpb3VzUGFnZSI6InNycCJ9; express:sess.sig=Y7sxOtC8gGxApT3aOV5Oyqrsyjo; s_nr=1580751226639; bucket=ypu%3Aypu%3Adefault; bucketsrc=default; TS0145ce01=01d0bb65df990d6b765e552cb75cabccf95014f60357fabf23e87d8bfa12df89f93c86f7de250189818d65cd1963bf1c08e0365afe66fd25a17684319e38b6c0451417466b; TS01cfebe6=01d0bb65dff326e70e6966e8bd77914d9af394eed32be487942c51d38d4bfeff0007359b6fbf67c908e41e0fd7100247e99628678e5cf54c1c5d449fd6ea39cc40c2f40a2aa0ce723da24dc5fb2661e8748553cf042a4bf8663c28bc71e6c74643ac9ef0c2818de13bd43df1565618710a0ffd2d9f64b00c03d8148ca049810cfe9af7fa88; _gat=1; zone=300; reese84=3:KZw7Y1E8VaCUg9FwE69eNQ==:nwa8E6bOExbVxzuRRLppWuQlUMw7OX4Nr/fjU+20WsUQIIuESjQm+B0vlU0LLVsc+pqb9YDAstMdvUrKreCbl7+fQStnArryfm5G8E4Hn2Gtptz4dM5z3PqU+fv8X3OYoOlfWYHeLRlg7phQO1FmQ899UHdF4dezkE/3zl/sYYlaf6l5RI4ZyEEw20O/40f62RdGPdTQe0rTQ/+Pakepzp4kwuGF+3aLKD0ZHyN2WhFaMgfbs0Bsewy/SDNs/twbh+lb0zue9C3CPTdcEZl+i5Y1JTWbzlMbg48iaAx4V2wzfG9Je6rxbEl9fcQSh8ihhQy3TSTsqE0AOa15ifAAKP9GIOeImeQKIOtbsRmOScDtZmatK4F74kkstZMlr7yspBYT3hLrcdfq7AOmZKIGzByj1MHIehjvvpdR/KAntvP2i4RSdcr89EtrVWGKYWxJ:7sdO6V9QvT9Fu60q97nyxhvwi2iE2kk5Q3McOzMg07o=; sorted=false; AMCVS_A57E776A5245AEA80A490D44%40AdobeOrg=1; AMCV_A57E776A5245AEA80A490D44%40AdobeOrg=-1303530583%7CMCIDTS%7C18296%7CMCMID%7C41080614554986137501106057387303695903%7CMCAAMLH-1581366415%7C3%7CMCAAMB-1581366415%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1580768815s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.3.0; s_tp=8062; s_ppv=search_results%2C8%2C8%2C663; s_cc=true',
            },
            meta={'download_timeout': 200},
            callback=self.tap_business_link
        )
   

    def tap_business_link(self, response):
        for b_name in response.xpath("//div[@class='result']/div/div/div/h2/a"):
            url= b_name.xpath(".//@href").get()
            absolute_url = response.urljoin(url)
            yield scrapy.Request(
                url=absolute_url,
                callback=self.parse
            )

        next_page_url = response.xpath("//a[contains(@class, 'next ajax-page')]/@href").get() 
        full_url = response.urljoin(next_page_url)
        yield scrapy.Request(
            url=full_url,
            callback=self.tap_business_link
        )  

    def parse(self, response):
        loader = ItemLoader(item=YellowpagesItem(), response=response)
        loader.add_xpath("business_name", "//h1/text()")
        loader.add_xpath("business_address", "//h2[@class='address']/text()")
        loader.add_xpath("phone_number", "//p[@class='phone']/text()")
        loader.add_xpath("email_address", "//a[@class='email-business']/@href")
        loader.add_xpath("fax", "(//dd[@class='extra-phones']/p/span)[2]/text()")
        loader.add_xpath("website", "//a[@class='primary-btn website-link']/@href")

        yield loader.load_item()
        
        
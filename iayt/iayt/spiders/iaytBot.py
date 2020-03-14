# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys

class IaytbotSpider(scrapy.Spider):
    name = 'iaytBot'

    responses = []
    page = 2

    def start_requests(self):

        yield SeleniumRequest(
            url='https://www.iayt.org/searchserver/people.aspx?id=7236F0DC-943F-4CF4-82E2-04B8EB7FE9EC&cdbid=&canconnect=0&canmessage=0&map=True&toggle=False&hhSearchTerms=',
            callback=self.parse,
            wait_time=10
        )

    def check(self, value):
        if int(value[0]) == 0:
            return int(value[1])
        else:
            return int(value)

    def parse(self, response):

        self.responses.append(response.body)

        driver = response.meta['driver']

        while True:
            next = driver.find_element_by_xpath(f"//a[text()={self.page}]")
            
            if next:                

                #next = check(next_hit.get_attribute('href')[52:54])
            
                print(len(self.responses))
                next.send_keys(Keys.ENTER)

                resp = Selector(text=driver.page_source)

                self.responses.append(resp)

                self.page += 1
            
            else:
                break



            


        
        



            

     
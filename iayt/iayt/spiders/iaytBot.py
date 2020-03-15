# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys

class IaytbotSpider(scrapy.Spider):
    name = 'iaytBot'

    responses = [] # To store all the responses when clicing on pagination.
    page = 2

    def start_requests(self):
        """
            The website has nested documents each inside iframe tag.
            Need to get the 'scr' for main data webpage, which changes frequently.
        """

        yield SeleniumRequest(
            url='https://www.iayt.org/search/newsearch.asp',
            callback=self.get_iframe_document_src,
            wait_time=5
        )

    def get_iframe_document_src(self, response):
        """
            Getting the url/src of data webpage and send a request to it.
        """

        iframe_document_src = response.xpath("//iframe[@id='SearchResultsFrame']/@src").get()
        iframe_document_src = response.urljoin(iframe_document_src)
        yield SeleniumRequest(
            url=iframe_document_src,
            callback=self.parse,
            wait_time=5
        )

    def parse(self, response): 

        # First page response added to the list.
        self.responses.append(response.body)

        # Getting the driver from response to handle pagination.
        driver = response.meta['driver']

        while True:
            """
                Trying to find the page link using the text associated with it.
                If failed then checking whether a page number is 11 because 
                every page displays pagination from 1 - 10 and 11 is shown as next
                so grabbing that in next try block.
                If pagination get completed then making a fake request and 
                extracting data from the list of responses.
            """
            try:
                next = driver.find_element_by_xpath(f"//a[text()={self.page}]")
            except:
                try:
                    next = driver.find_element_by_xpath("//img[contains(@src, 'pageRight')]/parent::node()")
                except:
                    return scrapy.Request(
                        url='https://iayt.org',
                        callback=self.extract_data
                    )  
            
            if next:                
                next.send_keys(Keys.ENTER)
                self.responses.append(driver.page_source)
                self.page += 1
         
    def extract_data(self, response):

        for each_response in self.responses:
            each_response_selector = Selector(text=each_response)
            for data in each_response_selector.xpath("//tr[@class='lineitem']"):
                yield {
                    'title': data.xpath('.//td/table/tbody/tr/td/div/a/text()').get(),
                    'city': data.xpath("((.//td[@valign='top'])[1]/div)[4]/text()").get(),
                    'state': data.xpath("((.//td[@valign='top'])[1]/div)[5]/text()").get(),
                    'code': data.xpath("((.//td[@valign='top'])[1]/div)[6]/text()").get(),
                    'country': data.xpath("((.//td[@valign='top'])[1]/div)[7]/text()").get(),
                    'img_url': data.xpath(".//a[@title='Photos in Profile']/img/@src").get(),
                    'url': data.xpath(".//td/table/tbody/tr/td/div/a/@href").get(),
                }





            


        
        



            

     
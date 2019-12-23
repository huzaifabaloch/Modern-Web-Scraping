# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class RankingbotSpider(scrapy.Spider):
    name = 'rankingbot'
    allowed_domains = ['www.reclameaqui.com.br']
    start_urls = ['https://www.reclameaqui.com.br/ranking']


    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=r"C:\Users\sunny ahmed\projects\selenium\drivers\chromedriver.exe", options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.reclameaqui.com.br/ranking")
        self.html = driver.page_source
        self.get_page_source(self.html)
        driver.close()

    def get_page_source(self, source):
        with open('page_source.txt', 'w') as file:
            file.write(source)

    def parse(self, response):
        resp = Selector(text=self.html)

        for table in resp.xpath("//div[@class='box-gray']"):
            for each in table.xpath("..//div[@class='box-gray']/ol/li"):
                yield {
                    'title': table.xpath("normalize-space(.//h2/text())").get(),
                    'date': table.xpath(".//p/text()").get(),
                    'reclamers': {
                        'name': each.xpath("normalize-space(.//div/a/text())").get(),
                        'percentage': each.xpath(".//div/a/span/text()").get()
                    }
                }
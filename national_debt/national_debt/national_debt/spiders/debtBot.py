# -*- coding: utf-8 -*-
import scrapy


class DebtbotSpider(scrapy.Spider):
    name = 'debtBot'
    allowed_domains = ['www.worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        
        countries= response.xpath("//table/tbody/tr")
        
        for country in countries:
            name = country.xpath(".//td[1]/a/text()").get()
            debt_to_gdp_ratio = country.xpath(".//td[2]/text()").get()

            yield {
                "country_name": name,
                "debt_to_gdp_ratio": debt_to_gdp_ratio
            }

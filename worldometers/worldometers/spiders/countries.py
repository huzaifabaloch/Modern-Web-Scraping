# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a")

        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            
            # Making target link as absolute from relative.
            # absolute_url = f"https://www.worldometers.info{link}"
            # absolute_url = response.urljoin(link)

            yield response.follow(url=link, callback=self.country_parse, meta={'country_name': name})

    def country_parse(self, response):
        # logging.info(response.url)

        country_name = response.request.meta["country_name"]
        country_population = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")

        for country in country_population:
            year = country.xpath(".//td[1]/text()").get()
            population = country.xpath(".//td[2]/strong/text()").get()

            yield {
                "country_name": country_name,
                'year': year,
                'population': population
            }


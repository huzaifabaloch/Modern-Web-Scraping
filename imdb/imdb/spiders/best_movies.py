# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['www.imdb.com']
    #start_urls = ['https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc']
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.imdb.com/search/title/?genres=drama&groups=top_250&sort=user_rating,desc',
            headers={'User-Agent': self.user_agent}
            )

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='lister-page-next next-page'])[2]"))
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        movie_name = response.xpath("//div[@class='title_wrapper']/h1/text()[1]").get()
        movie_year = response.xpath("//div[@class='title_wrapper']/h1/span/a/text()").get()
        duration = response.xpath("//div[@class='title_wrapper']/div/time/text()").get().strip()
        genre = response.xpath("//div[@class='title_wrapper']/div/a[1]/text()").get()
        rating = response.xpath("//strong/span/text()").get()
        movie_url = response.url

        yield{
            'movie_name': movie_name,
            'movie_year': movie_year,
            'duration': duration,
            'genre': genre,
            'rating': rating,
            'movie_url': movie_url,
        }
        
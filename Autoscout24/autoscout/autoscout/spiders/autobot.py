# -*- coding: utf-8 -*-
import scrapy


class AutobotSpider(scrapy.Spider):
    name = 'autobot'
    allowed_domains = ['www.autoscout24.de']
    start_urls = ['https://www.autoscout24.de/lst?sort=standard&desc=0&ustate=N%2CU&cy=D&priceto=5000&atype=C']
    page_num = 1
    total_pages = 5

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.autoscout24.de/lst?sort=standard&desc=0&ustate=N%2CU&cy=D&priceto=5000&atype=C',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            },
            callback=self.parse
        )

    def parse(self, response):

        with open('rsp.html', 'wb') as f:
            f.write(response.body)

        for rel_url in response.xpath("//a[@data-item-name='detail-page-link']"):
            abs_url = response.urljoin(rel_url.xpath('.//@href').get())
            yield scrapy.Request(
                url=abs_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                },
                callback=self.extract_data
            )
        
        if self.page_num <= self.total_pages:
            self.page_num += 1
            next_url = f'https://www.autoscout24.de/lst/?sort=standard&desc=0&ustate=N%2CU&size=20&page={self.page_num}&cy=D&priceto=5000&atype=C&fc={self.page_num-1}&qry=&'
            yield scrapy.Request(
                url=next_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                },
                callback=self.parse
            )

    def extract_data(self, response):

        yield {
            'make_model': response.xpath("(//span[@class='cldt-detail-makemodel sc-ellipsis'])[1]/text()").get(),
            'detail_version': response.xpath("(//span[@class='cldt-detail-version sc-ellipsis'])[1]/text()").get(),
            'price_in_euro': response.xpath("normalize-space((//div[@class='cldt-price '])[2]/h2/text())").get().split(',')[0],
            'phone_number': response.xpath("//a[@name='stickyCallButton']/text()").get().split(')')[1]
        }
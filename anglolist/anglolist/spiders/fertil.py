import scrapy 


class FertilSpider(scrapy.Spider):
    name = 'fertil'

    def start_requests(self):
        yield scrapy.Request(
            url='https://translate.google.com/translate?sl=auto&tl=en&u=https%3A%2F%2Ffertilitycentercolombia.com%2F',
            cookies={
                'googtrans': '/es/en'
            },
            callback=self.parse
        )


    def parse(self, response):

        with open('ind.html', 'wb') as f:
            f.write(response.body)
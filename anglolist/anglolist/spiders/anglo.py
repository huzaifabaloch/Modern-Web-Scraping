import scrapy


class AngloSpider(scrapy.Spider):
    name = 'anglo'
    headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}


    def start_requests(self):
        yield scrapy.Request(
            url='https://www.anglo-list.com/category/health-medical-wellbeing-beauty',
            callback=self.get_links,
            headers=self.headers
        )

    def get_links(self, response):
        
        for link in response.xpath("//h3[@class='business-name']/a"):
            yield scrapy.Request(
                url=link.xpath(".//@href").get(),
                callback=self.parse,
                headers=self.headers
            )

        
        next_url = response.xpath("//a[@title='Next']/@href").get()
        if next_url:
            abs_url = response.urljoin(next_url)
            yield scrapy.Request(
                url=abs_url,
                headers=self.headers,
                callback=self.get_links
            )
    
    def parse(self, response):

        yield {
            'business_name': response.xpath("normalize-space(//h1[@itemprop='name']/text())").get(),
            'address': response.xpath("normalize-space((//span[@itemprop='address']/text())[last()])").get(),
            'telephone': response.xpath("//span[@itemprop='telephone']/a/text()").get(),
            'email': response.xpath("normalize-space((//span[@itemprop='email']/text())[last()])").get(),
            'website': response.xpath("//a[@class='website']/@href").get()
        }

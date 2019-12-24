import scrapy
import json

class RankingsByApi(scrapy.Spider):
    name = 'ranksbyapi'
    #allowed_domains = ['www.reclameaqui.com.br']

    def start_requests(self):
        yield scrapy.Request(
            url='https://iosite.reclameaqui.com.br/raichu-io-site-v1/company/rankings/20',
            callback=self.parse_json,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            },
            meta={
                "Accept": "application/json, text/plain,",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
                "Connection": "keep-alive",
                "Host": "iosite.reclameaqui.com.br",
                "Origin": "https://www.reclameaqui.com.br",
                "Referer": "https://www.reclameaqui.com.br/ranking",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site"
            }
        )

    def parse_json(self, response):
        data = json.loads(response.body)
        count = 0
        for each_company in data.get('topSolvingOf30Days'):
            yield scrapy.Request(
                url='https://iosite.reclameaqui.com.br/raichu-io-site-v1/company/shortname/{}'.format(each_company.get('companyShortname')),
                headers={   
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
                },
                meta={
                'Host': 'iosite.reclameaqui.com.br',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain,',
                'Origin': 'https://www.reclameaqui.com.br',
                'Sec-Fetch-Site': 'same-site',
                'Sec-Fetch-Mode': 'cors',
                "Referer": "https://www.reclameaqui.com.br/empresa/{}".format(response.url),
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8'
                }
            )
            
       
    def parse(self, response):
        data = json.loads(response.body)

        company_name = data.get('companyName')

        for each_type in data.get('panels'):

            avg = each_type.get('avg')
            created =  each_type.get('index').get('created')        
            start = each_type.get('index').get('start')                
            averageAnswerTime =  each_type.get('index').get('averageAnswerTime')        
            finalScore =  each_type.get('index').get('finalScore')        
            totalNotAnswered =  each_type.get('index').get('totalNotAnswered')        
            totalComplains =  each_type.get('index').get('totalComplains')        
            consumerScore =  each_type.get('index').get('consumerScore')        
            type =  each_type.get('index').get('type')        
            answeredPercentual =  each_type.get('index').get('answeredPercentual')        
            status =  each_type.get('index').get('status')        
            totalEvaluated =  each_type.get('index').get('totalEvaluated')     


            yield {
                'type': {
                    'companyName': company_name,
                    'type': type,
                    'created': created,
                    'start': start,
                    'avg': avg,
                    'averageAnswerTime': averageAnswerTime,
                    'finalScore': finalScore,
                    'totalNotAnswered': totalNotAnswered,
                    'totalComplains': totalComplains,
                    'consumerScore': consumerScore,
                    'answeredPercentual': answeredPercentual,
                    'status': status,
                    'totalEvaluated': totalEvaluated
                }
            }   

        

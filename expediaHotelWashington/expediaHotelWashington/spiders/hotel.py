# -*- coding: utf-8 -*-
import scrapy
import json

class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['www.expedia.com']
    count = 50
    starting_index = 100

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.expedia.com/hotel-shop/api/1/en_US/hotels?accessibility=&amenities=&deals=&destination=Washington%20(and%20vicinity)%2C%20District%20of%20Columbia%2C%20United%20States%20of%20America&endDate=2020-02-04&latLong=38.90261%2C-77.02277&lodging=&paymentType=&price=&regionId=178318&sort=RECOMMENDED&star=&startDate=2020-01-11&travelerType=&useRewards=true&bedroomFilter=&propertyStyle=&rewards=&localDateFormat=M%2Fd%2Fyyyy&adults=3&children=1_5%2C1_7%2C1_6%2C1_9%2C1_5%2C1_9',
            headers= {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
                'x-api-token': '7afd86895ffacb830d583bc10b99c91dd4664b10',
                'Cookie': 'urrency=USD; linfo=v.4,|0|0|255|1|0||||||||1033|0|0||0|0|0|-1|-1; MC1=GUID=63394084548b415fbd14c968f0bd0ae9; DUAID=63394084-548b-415f-bd14-c968f0bd0ae9; stop_mobi=yes; s_ecid=MCMID%7C37229176197230612180428176955250319883; AB_Test_TripAdvisor=A; rlt_marketing_code_cookie=; intent_media_prefs=; __gads=ID=46640596ca8569b2:T=1574101253:S=ALNI_Mb8RG1xYwMFaafE7XSVEcLSWEzL7A; _gcl_au=1.1.1028329342.1574101247; _ga=GA1.2.680080315.1574101240; _fbp=fb.1.1574101250568.618808542; xdid=260472b3-e193-4989-99ec-2c274978eceb|1574101264|expedia.com; kppid_managed=NBg7z8MN; aspp=v.1,0|network.cj.9126416.10829941.135909X1599316X92ffe58b092a08c71541d92263dc933d|||||||||AFF|20191219||; tpid=v.1,1; _gid=GA1.2.1427282045.1578723490; lastConsentChange=1578723492110; IM_eu_freq_cap=Y; iEAPID=0; ipsnf3=v.3%7Cus%7C1%7C753%7Cchandler; AMCVS_C00802BE5330A8350A490D4C%40AdobeOrg=1; AMCV_C00802BE5330A8350A490D4C%40AdobeOrg=1406116232%7CMCIDTS%7C18273%7CMCMID%7C37229176197230612180428176955250319883%7CMCAAMLH-1579347433%7C3%7CMCAAMB-1579347433%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1578749833s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C2.5.0%7CMCCIDH%7C-2034012538; s_cc=true; CONSENTMGR=ts:1578742634830%7Cconsent:true; qualtrics_sample=false; qualtrics_SI_sample=false; JSESSION=941ca8ff-d833-4357-8049-8e92540e455b; _tq_id.TV-721872-1.7ec4=96091fffbb6a452e.1574101248.0.1578742642..; IM_xu_2_fq=Y; pwa_csrf=c2ad2f44-2fc1-422f-a0a1-f0d897f3374d|PPk8fZ9qj8GJB_GGieQFS-jf2tgEsppRiy1l6cFA0Hf-yFFL-6CCjtAlTRV5Q9T2LeLDPgpuspNYS8c_kJX6QQ; JSESSIONID=D443C4D98C365FB9B5B7DB8F9638CEC2; cesc=%7B%22marketingClick%22%3A%5B%22false%22%2C1578745748018%5D%2C%22hitNumber%22%3A%5B%226%22%2C1578745748018%5D%2C%22visitNumber%22%3A%5B%225%22%2C1578745219313%5D%2C%22entryPage%22%3A%5B%22page.Hotel-Search%22%2C1578745748018%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1578723473111%5D%7D; s_ppvl=page.Hotel-Search%2C16%2C13%2C663%2C1366%2C663%2C1366%2C768%2C1%2CP; s_ppv=page.Hotel-Search%2C100%2C15%2C10136%2C1366%2C663%2C1366%2C768%2C1%2CP; utag_main=v_id:016e7fbeb23b0072f42d86b17b500307101030690086e$_sn:5$_ss:0$_st:1578748549721$_pn:6%3Bexp-session$ses_id:1578742634876%3Bexp-session',
            },
            callback=self.parse
        )

    def store_raw_data(self, response):
        data = json.loads(response.body)
        with open('raw.json', 'w') as file:
            file.write(json.dumps(data))

    def parse(self, response):
        hotels_data = json.loads(response.body)

        for hotel in hotels_data.get('hotels'):
            try:
                yield {
                    'hotel_name': hotel.get('hotelName'),
                    'review': hotel.get('reviews').get('localizedCount'),
                    'rating': hotel.get('reviews').get('localizedOverallRating'),
                    'remark': hotel.get('reviews').get('superlative'),
                    'check_in': hotel.get('shortlistModel').get('clickTracking')[0].get('messageContent').get('tripStartDate'),
                    'check_out': hotel.get('shortlistModel').get('clickTracking')[0].get('messageContent').get('tripEndDate'),
                    'no_of_adult': hotel.get('shortlistModel').get('clickTracking')[0].get('messageContent').get('numAdults'),
                    'no_of_children': hotel.get('shortlistModel').get('clickTracking')[0].get('messageContent').get('numChildren'),
                    'no_of_room': hotel.get('shortlistModel').get('clickTracking')[0].get('messageContent').get('shoppingHotel').get('numRooms'),
                }
            except AttributeError:
                pass


        total_count = hotels_data.get('totalPropertyCount')
        if self.count <= total_count:
            next_page = f'https://www.expedia.com/hotel-shop/api/1/en_US/hotels?accessibility=&amenities=&deals=&destination=Washington%20(and%20vicinity)%2C%20District%20of%20Columbia%2C%20United%20States%20of%20America&endDate=2020-02-04&latLong=38.90261%2C-77.02277&lodging=&paymentType=&price=&regionId=178318&sort=RECOMMENDED&star=&startDate=2020-01-11&travelerType=&useRewards=true&bedroomFilter=&propertyStyle=&rewards=&localDateFormat=M%2Fd%2Fyyyy&count={self.count}&startingIndex={self.starting_index}&adults=3&children=1_5%2C1_7%2C1_6%2C1_9%2C1_5%2C1_9'
            self.count += 50
            self.starting_index += 50
            yield scrapy.Request(
                url=next_page,
                headers= {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
                'x-api-token': '7afd86895ffacb830d583bc10b99c91dd4664b10',
                'Cookie': 'urrency=USD; linfo=v.4,|0|0|255|1|0||||||||1033|0|0||0|0|0|-1|-1; MC1=GUID=63394084548b415fbd14c968f0bd0ae9; DUAID=63394084-548b-415f-bd14-c968f0bd0ae9; stop_mobi=yes; s_ecid=MCMID%7C37229176197230612180428176955250319883; AB_Test_TripAdvisor=A; rlt_marketing_code_cookie=; intent_media_prefs=; __gads=ID=46640596ca8569b2:T=1574101253:S=ALNI_Mb8RG1xYwMFaafE7XSVEcLSWEzL7A; _gcl_au=1.1.1028329342.1574101247; _ga=GA1.2.680080315.1574101240; _fbp=fb.1.1574101250568.618808542; xdid=260472b3-e193-4989-99ec-2c274978eceb|1574101264|expedia.com; kppid_managed=NBg7z8MN; aspp=v.1,0|network.cj.9126416.10829941.135909X1599316X92ffe58b092a08c71541d92263dc933d|||||||||AFF|20191219||; tpid=v.1,1; _gid=GA1.2.1427282045.1578723490; lastConsentChange=1578723492110; IM_eu_freq_cap=Y; iEAPID=0; ipsnf3=v.3%7Cus%7C1%7C753%7Cchandler; AMCVS_C00802BE5330A8350A490D4C%40AdobeOrg=1; AMCV_C00802BE5330A8350A490D4C%40AdobeOrg=1406116232%7CMCIDTS%7C18273%7CMCMID%7C37229176197230612180428176955250319883%7CMCAAMLH-1579347433%7C3%7CMCAAMB-1579347433%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1578749833s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C2.5.0%7CMCCIDH%7C-2034012538; s_cc=true; CONSENTMGR=ts:1578742634830%7Cconsent:true; qualtrics_sample=false; qualtrics_SI_sample=false; JSESSION=941ca8ff-d833-4357-8049-8e92540e455b; _tq_id.TV-721872-1.7ec4=96091fffbb6a452e.1574101248.0.1578742642..; IM_xu_2_fq=Y; pwa_csrf=c2ad2f44-2fc1-422f-a0a1-f0d897f3374d|PPk8fZ9qj8GJB_GGieQFS-jf2tgEsppRiy1l6cFA0Hf-yFFL-6CCjtAlTRV5Q9T2LeLDPgpuspNYS8c_kJX6QQ; JSESSIONID=D443C4D98C365FB9B5B7DB8F9638CEC2; cesc=%7B%22marketingClick%22%3A%5B%22false%22%2C1578745748018%5D%2C%22hitNumber%22%3A%5B%226%22%2C1578745748018%5D%2C%22visitNumber%22%3A%5B%225%22%2C1578745219313%5D%2C%22entryPage%22%3A%5B%22page.Hotel-Search%22%2C1578745748018%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1578723473111%5D%7D; s_ppvl=page.Hotel-Search%2C16%2C13%2C663%2C1366%2C663%2C1366%2C768%2C1%2CP; s_ppv=page.Hotel-Search%2C100%2C15%2C10136%2C1366%2C663%2C1366%2C768%2C1%2CP; utag_main=v_id:016e7fbeb23b0072f42d86b17b500307101030690086e$_sn:5$_ss:0$_st:1578748549721$_pn:6%3Bexp-session$ses_id:1578742634876%3Bexp-session',
                },
                callback=self.parse
            )

        

        
        


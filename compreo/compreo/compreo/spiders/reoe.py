# -*- coding: utf-8 -*-
import scrapy
import json

class ReoeSpider(scrapy.Spider):
    name = 'reo'
    
    url = "https://www.compreoalquile.com/rplis-api/postings"

    payload = "{\n    \"q\": null,\n    \"direccion\": null,\n    \"moneda\": null,\n    \"preciomin\": null,\n    \"preciomax\": null,\n    \"services\": \"\",\n    \"general\": \"\",\n    \"roomType\": \"\",\n    \"outside\": \"\",\n    \"areaPrivativa\": \"\",\n    \"areaComun\": \"\",\n    \"multipleRets\": \"\",\n    \"tipoDePropiedad\": \"2\",\n    \"tipoDeOperacion\": \"1\",\n    \"garages\": null,\n    \"antiguedad\": null,\n    \"expensasminimo\": null,\n    \"expensasmaximo\": null,\n    \"ambientes\": null,\n    \"habitaciones\": null,\n    \"banos\": null,\n    \"superficieCubierta\": 1,\n    \"idunidaddemedida\": 1,\n    \"metroscuadradomin\": null,\n    \"metroscuadradomax\": null,\n    \"tipoAnunciante\": null,\n    \"grupoTipoDeMultimedia\": null,\n    \"publicacion\": null,\n    \"sort\": \"relevance\",\n    \"etapaDeDesarrollo\": null,\n    \"auctions\": null,\n    \"polygonApplied\": null,\n    \"pagina\": 1,\n    \"subtipoDePropiedad\": null,\n    \"city\": \"\",\n    \"province\": \"\",\n    \"zone\": \"\",\n    \"valueZone\": \"\",\n    \"subZone\": \"\",\n    \"coordenates\": null\n}"
    headers = {
    'x-requested-with': 'XMLHttpRequest',
    'content-type': 'application/json',
    'cookie': '__cfduid=db9f84c216bb252506106f6cb02fa6f821589098378; _ga=GA1.2.941071275.1589098377; _gid=GA1.2.993907175.1589098377; sessionId=9c20b01c-9eed-4778-998a-5856183ff582; G_ENABLED_IDPS=google; __gads=ID=1818665fe960a641:T=1589098387:S=ALNI_Ma7OojlFMbFVo5uP77f5onLHpBGgQ; _fbp=fb.1.1589098391619.2086484345; _hjid=86934e98-7351-47ec-a6a2-29e55e977d7b; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmbj2=1589098419; __uzmaj2=86459820-b85f-4ae7-9d6b-0297d962c4b4; __uzma=ff666b7d-1d8e-450f-972f-60de99c5300f; __uzmb=1589098572; _hjIncludedInSample=1; operationId=1; realEstateTypeId=2; ambientes=; precioMin=; idciudad=; mapView=; searchboxText=; precioMax=; idsubzonaciudad=; idzonavalor=; idprovincia=; idzonaciudad=; __uzmc=984201690290; __uzmd=1589134147; showMoreFilters=true; __uzmcj2=725323432777; __uzmdj2=1589148605; _dc_gtm_UA-5187873-1=1; JSESSIONID=9753DA5BFEDB37D3B3BA7499E8EF5AE1; _gat_UA-5187873-1=1',
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=27F578FFEC381406374F50EB1DB7E1F5; __uzmc=647973119666; __uzmd=1589148779'
    }

    cur_page = 1


    def start_requests(self):
        yield scrapy.Request(
            url=self.url,
            headers=self.headers,
            method='POST',
            body=self.payload,
            callback=self.parse
        )

    def parse(self, response):

        data_feed = json.loads(response.body)

        for posting in data_feed.get('listPostings'):

            if 'm²' in posting.get('generatedTitle'):
                is_size_in_generated_title = posting.get('generatedTitle')
                size_m2 = is_size_in_generated_title.split('·')[1].strip().replace('m²', '')

            elif posting.get('units'):
                size = 0
                for unit in posting.get('units'):
                    if unit.get('mainFeatures').get('CFT100'):
                        if unit.get('mainFeatures').get('CFT100').get('value'):
                            c_size = int(unit.get('mainFeatures').get('CFT100').get('value'))
                            if size < c_size:
                                size = c_size
                if size != 0:
                    size_m2 = str(size)
                else:
                    size_m2 = ''

            else:
                size_m2 = ''

            
            title = posting.get('title')
            price = posting.get('priceOperationTypes')[0].get('prices')[0].get('amount')


            if posting.get("postingLocation"): 
                if posting.get('postingLocation').get('postingGeolocation'):
                    if posting.get('postingLocation').get('postingGeolocation').get('geolocation') is not None:
                        latitude = posting.get('postingLocation').get('postingGeolocation').get('geolocation').get('latitude')
                        longitude = posting.get('postingLocation').get('postingGeolocation').get('geolocation').get('longitude')
                    else:
                        latitude = None
                        longitude = None
                else:
                    latitude = None
                    longitude = None
            else:
                latitude = None
                longitude = None


            yield {
                'title': title,
                'size_m2': size_m2,
                'price': price,
                'latitude': latitude,
                'longitude': longitude
            }
            

        
        total_pages = data_feed.get('paging').get('totalPages')

        if self.cur_page < total_pages:
            self.cur_page += 1
            self.payload = "{\n    \"q\": null,\n    \"direccion\": null,\n    \"moneda\": null,\n    \"preciomin\": null,\n    \"preciomax\": null,\n    \"services\": \"\",\n    \"general\": \"\",\n    \"roomType\": \"\",\n    \"outside\": \"\",\n    \"areaPrivativa\": \"\",\n    \"areaComun\": \"\",\n    \"multipleRets\": \"\",\n    \"tipoDePropiedad\": \"2\",\n    \"tipoDeOperacion\": \"1\",\n    \"garages\": null,\n    \"antiguedad\": null,\n    \"expensasminimo\": null,\n    \"expensasmaximo\": null,\n    \"ambientes\": null,\n    \"habitaciones\": null,\n    \"banos\": null,\n    \"superficieCubierta\": 1,\n    \"idunidaddemedida\": 1,\n    \"metroscuadradomin\": null,\n    \"metroscuadradomax\": null,\n    \"tipoAnunciante\": null,\n    \"grupoTipoDeMultimedia\": null,\n    \"publicacion\": null,\n    \"sort\": \"relevance\",\n    \"etapaDeDesarrollo\": null,\n    \"auctions\": null,\n    \"polygonApplied\": null,\n    \"pagina\": %s,\n    \"subtipoDePropiedad\": null,\n    \"city\": \"\",\n    \"province\": \"\",\n    \"zone\": \"\",\n    \"valueZone\": \"\",\n    \"subZone\": \"\",\n    \"coordenates\": null\n}" %(self.cur_page)
 
            yield scrapy.Request(
                url=self.url,
                headers=self.headers,
                method='POST',
                body=self.payload,
                callback=self.parse
            )













                #     yield {
                #         'title': posting.get('title'),

                #         'from_size_m2': posting.get('units')[3].get('mainFeatures').get('CFT101').get('value'),
                #         'to_size_m2': posting.get('units')[1].get('mainFeatures').get('CFT101').get('value'),

                #         'price': posting.get('priceOperationTypes')[0].get('prices')[0].get('amount'),
                #         'latitude': posting.get('postingLocation').get('postingGeolocation').get('geolocation').get('latitude'),
                #         'longitude': posting.get('postingLocation').get('postingGeolocation').get('geolocation').get('longitude'),
                #     }

                # else:
                #     yield {
                #         'title': posting.get('title'),
                #         'from_size_m2': posting.get('units')[3].get('mainFeatures').get('CFT101').get('value'),
                #         'to_size_m2': posting.get('units')[1].get('mainFeatures').get('CFT101').get('value'),
                #         'price': posting.get('priceOperationTypes')[0].get('prices')[0].get('amount'),
                #         'latitude': None,
                #         'longitude': None,
                #     }
                
                # except:


                

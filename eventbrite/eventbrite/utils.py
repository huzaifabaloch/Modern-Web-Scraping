from http.cookies import SimpleCookie
import json

def cookie_parser():
    "Cookie string to Pythion Dict for best practise"

    cookie_string = "mgrefby=; G=v%3D2%26i%3D04a6a593-b419-451f-9ac7-8912a963e9b4%26a%3Dc6c%26s%3Dd5758d1aa25c0cfb0796627ab2a0d2e3b3e89548; ebEventToTrack=; eblang=lo%3Den_US%26la%3Den-us; AN=; mgref=typeins; csrftoken=dbb779f036e411eab665ef1f6bf713f4; _ga=GA1.2.687545818.1579016719; ebGAClientId=687545818.1579016719; _gaexp=GAX1.2.VMDdMrAiSGGJcy4TVI4fsA.18364.1; mgaff55392014005=ebdssbdestsearch; mgref=eafil; _gcl_au=1.1.440292761.1579025793; _fbp=fb.1.1579025797117.1453060398; mgaff55392014005=ebdssbdestsearch; mgaff62042651240=ebdssbdestsearch; mgaff62042651240=ebdssbdestsearch; _gid=GA1.2.1416921008.1580542895; cm=%5B55392014005%2C%2062042651240%2C%2059806133756%5D; mgaff59806133756=ebdssbdestsearch; location=%7B%22place_id%22%3A%20%2285675757%22%2C%20%22place_type%22%3A%20%22region%22%2C%20%22current_place_parent%22%3A%20%22Pakistan%22%2C%20%22longitude%22%3A%2067.0817%2C%20%22current_place%22%3A%20%22Sind%22%2C%20%22latitude%22%3A%2024.9043%2C%20%22slug%22%3A%20%22pakistan--sind%22%7D; SS=AE3DLHRy29gCfxgoC65RMd4NUyR0fKfVlQ; AS=f058e537-bb32-4174-95ba-dd17c01dbc12; SERVERID=djc65; location={%22slug%22:%22ca--san-francisco%22%2C%22place_id%22:%2285922583%22%2C%22latitude%22:37.7749295%2C%22longitude%22:-122.4194155%2C%22place_type%22:%22locality%22%2C%22current_place%22:%22San%20Francisco%22%2C%22current_place_parent%22:%22CA%2C%20USA%22}; janus=v%3D1%26exp_eb_127335_derank_sold_out_events_in_search%3DNone%26exp_eb_search_experiment_3%3DNone%26exp_eb_search_experiment_4%3DNone; _gat=1; SP=AGQgbbkb5CmmDaCwICI-QnIgILw5NV9aFE-nz2pTsqtbDWUOlQp8tOVc2DuUaBxdmQc_AWUrEqrOxcuyrsrErj51bJ3OPy13zsy3aTVzE2ZSn112LLk-4Mp9BZiGzsbMKAqY0XQqGJyyGW4XAgJlbtK8jK4nE9EhBbjZmtTlSwseiARBRGyNh20NgFQp8GO7-rLOM7TraWEg_98-W9mhNFD4wrF09D-uq1DuqKmSNwfdD8N5PxaUz-w"
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    cookies = {}

    for key, morsel in cookie.items():
        cookies[key] = morsel

    return cookies




def minimum_ticket(price):
    if price.get('is_free') == 'false':
        return price.get('minimum_ticket_price').get('major_value')
      
    else:
        return 'free'


dic = {
    
                    "is_sold_out": false,
                    "is_free": false,
                    "minimum_ticket_price": {
                        "currency": "USD",
                        "value": 2500,
                        "major_value": "25.00",
                        "display": "25.00 USD"
                    }
}


print(minimum_ticket(dic))
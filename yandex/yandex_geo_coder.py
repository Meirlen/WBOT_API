import json
import requests
from yandex.json_data import *
from yandex.yandex_config import *


from yandex.calc_price import get_saved_last_token

def get_address_by_coords(lat,lon):

    route_array = []




    json_data = geo_coder_json_data
    json_data['state']['location'] = [lat,lon]
    json_data['position'] = [lat,lon]

    
    json_data['id'] = x_yataxi_userid
 
    print(json_data)

    # set csrf token
    x_csrf_token = os.getenv("CSRF_TOKEN",None)
    x_csrf_token = get_saved_last_token()

    headers['x-csrf-token'] =  x_csrf_token

    response = requests.post('https://ya-authproxy.taxi.yandex.kz/integration/turboapp/v1/suggest', cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)

    
    print(response.status_code)
    if response.status_code == 400:
        print("Order creating ERROR")

        print(text)
    if response.status_code == 401:
        print("Unauthorized 401")
    if response.status_code == 200:  
        print(text['results'][0]['title']['text'])
        return text['results'][0]['title']['text']

    return None
    
import json
import requests
from yandex.json_data import *
from yandex.yandex_config import * 
from yandex.data_models import *

def get_price_by_route(routes):

    result = None

    json_data = calc_price_json_data
    json_data['id'] = x_yataxi_userid
    json_data["route"] = routes

    response = requests.post('https://ya-authproxy.taxi.yandex.ru/3.0/routestats', cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)



    print(text)
    print(response.status_code)

    if response.status_code == 401:
        print("Unauthorized 401")
    if response.status_code == 200:
        result = [] 
        for trip_type in text['service_levels']:
            trip_price = trip_type['price'].replace('$SIGN$$CURRENCY$', 'T')
            result.append({"name_tariff": trip_type['name'],"price":trip_price})
            print(f"{trip_type['name']} - {trip_price}")



    return result





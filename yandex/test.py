import json
import requests
from json_data import *
from yandex_config import *


# route = [
#                 {
#                 "short_text": "улица Алиханова, 13",
#                 "geopoint": [
#                     73.088504,
#                     49.807754
#                 ],
#                 "fullname": "Караганда, улица Алиханова, 13",
#                 },
#                 {
#                 "short_text": "Ясли-сад Еркетай",
#                 "geopoint": [
#                     73.151855,
#                     49.782448
#                 ],
#                 "fullname": "Казахстан, Караганда, микрорайон Степной-1, 7А, Ясли-сад Еркетай",
#                 }
#             ]



def create_draft(routes):

    json_data = create_draft_json_data
    json_data['id'] = x_yataxi_userid
    json_data["route"] = routes

    response = requests.post('https://ya-authproxy.taxi.yandex.ru/external/3.0/orderdraft', cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)

    # print(text)
    print(response.status_code)

    if response.status_code == 401:
        print("Unauthorized 401")
    if response.status_code == 200:  
        order_id = text["orderid"]
        print(order_id)
        print("Order Draft succesfully created")

        return order_id

    return None


create_draft(route)
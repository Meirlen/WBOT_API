
import json
import requests
from yandex.json_data import *
from yandex.yandex_config import *


# route = [
#                 {
#                 "short_text": "улица Алиханова, 13",
#                 "geopoint": [
#                     73.088504,
#                     49.807754
#                 ],
#                 "fullname": "Караганда, улица Алиханова, 13",
#                 "type": "address",
#                 "city": "Караганда",
#                 },
#                 {
#                 "short_text": "Ясли-сад Еркетай",
#                 "geopoint": [
#                     73.151855,
#                     49.782448
#                 ],
#                 "fullname": "Казахстан, Караганда, микрорайон Степной-1, 7А, Ясли-сад Еркетай",
#                 "type": "organization",
#                 "city": "Караганда",
#                 }
#             ]
def send_order_to_yandex(routes,client_phone_number):
    print(send_order_to_yandex)

    route_array = []


    for route in routes:

        point_type = 'organization'

        if route.type == "geo":
            point_type = 'address'
        route_array.append({
                                "short_text": route.short_text,
                                "geopoint": [
                                    round(route.geo_point[0], 6),
                                    round(route.geo_point[1], 6),
                                ],
                                "fullname": route.fullname,
                                "type": point_type,
                                "city":  route.city
                            })

    json_data = create_draft_json_data
    json_data['id'] = x_yataxi_userid
    json_data["route"] = route_array
    json_data["extra_contact_phone"] = client_phone_number

    print(json_data)

    # set csrf token
    x_csrf_token = os.getenv("CSRF_TOKEN",None)
    headers['x-csrf-token'] =  x_csrf_token

    response = requests.post('https://ya-authproxy.taxi.yandex.ru/external/3.0/orderdraft', cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)

    
    print(response.status_code)
    if response.status_code == 400:
        print("Order creating ERROR")

        print(text)
    if response.status_code == 401:
        print("Unauthorized 401")
    if response.status_code == 200:  
        order_id = text["orderid"]
        print(order_id)
        print("Order Draft succesfully created")
        order_commit(order_id)
        return order_id

    return None
    
   
 


def order_commit(order_id):

    json_data = {
                "id": x_yataxi_userid,       # x-yataxi-userid
                "orderid": order_id
                }


    # set csrf token
    x_csrf_token = os.getenv("CSRF_TOKEN",None)
    headers['x-csrf-token'] =  x_csrf_token
    
    response = requests.post('https://ya-authproxy.taxi.yandex.ru/external/3.0/ordercommit', cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)
    print(response.status_code)
    print(text)

    

    if response.status_code == 401:
        print("Unauthorized 401")
    if response.status_code == 406:  
        print("PRICE_CHANGED , Цена изменилась. Повторите попытку.'")  
    if response.status_code == 200:  
       print("Отлично,  мы начали поиск авто  , Status: ",  text["status"])




       

# create_draft()
# # order_commit("4d2476f5885a315f87888f1a43d0904e")
import requests
import time
import datetime
from yandex.json_data import *
import json



def get_order(order_id, cancel = False):


    json_data = {
                "format_currency": True,
                "id": x_yataxi_userid,      
                "orderid": order_id
                }

    if cancel:
       json_data["break"] = "user"            

    response = requests.post('https://stackoverflow.com/', cookies=cookies, headers=headers,
                             json=json_data)

    # text = json.loads(response.text)

    print(response.status_code)


    

while True :

    print("get request")

    searh_car_status_orders_ids = ['a','b','c','d','e','j','k','l','m','n','o']

    if len(searh_car_status_orders_ids) > 0:
        start = datetime.datetime.now()

        for order_id in searh_car_status_orders_ids:
            print('request: ' , order_id) 
            get_order(order_id)

        finish = datetime.datetime.now()
        print("Speed : ",finish-start)



    time.sleep(10)
        # get_order("dfc0160863cdc4febd3add5e742b74b6")






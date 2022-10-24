import json
import requests
from yandex.json_data import *
from yandex.yandex_config import *



def get_order(order_id, cancel = False):
    json_data = {
                "format_currency": True,
                "id": x_yataxi_userid,      
                "orderid": order_id
                }

    if cancel:
       json_data["break"] = "user"            

    response = requests.post('https://ya-authproxy.taxi.yandex.ru/3.0/taxiontheway', cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)

    print(text)
    print(response.status_code)

    if response.status_code == 401:
        print("Unauthorized 401")

    if response.status_code == 404:
        print("Order not found")    
    if response.status_code == 200:  
        print(text)
        print("СТАТУС ПОИСКА: ",text["status"])
        status = text["status"]

        if status == "search":
            print("Идет поиск машины: " )
        if status == "assigned":
            print("Водитель назначен: ", driver)

        if status == "driving":
           driver  = text["driver"] 
           driver_name = driver['name']
           car_color = driver['color']
           car_model = driver['model']
           plates = driver['125АВР09']
           rating = driver['rating']
           phone_num = driver['forwarding']['phone']


           print("К Вам выехал " , car_color, ' ', car_color , ',  гос номер:' ,plates )
           print("О водителе: " , driver_name, ',', phone_num )

        if status == "cancelled":
            print("Заказ отменен клиентом: ")  
        if status == "expired":
           print("Машина не найдена")



from dataclasses import dataclass

@dataclass
class OrderInfo:
    yandex_order_id:str
    status:str
    order_id:int
    fb_token:str



@dataclass
class DriverInfo:
    full_name:str
    car_info:str
    phone_num:str
    final_cost:str
    title:str = None

import json
import aiohttp
import asyncio
import time
from yandex.json_data import *
from yandex.yandex_config import *
from app.database import get_db
from app import models, schemas as schemas
from app.wati_msg_builder import *
import os
from yandex.calc_price import get_saved_last_token
from yandex.order_crud_status import update_order_status_in_db_and_fb,driver_not_found_info_in_db_and_fb,update_order_driver_lat_lng

async def get_order(session, order_info:OrderInfo):

    url = 'https://ya-authproxy.taxi.yandex.ru/3.0/taxiontheway'


    # set csrf token
    # x_csrf_token = os.getenv("CSRF_TOKEN",None)

    # if x_csrf_token == None:
    x_csrf_token = get_saved_last_token()
    os.environ["CSRF_TOKEN"] = x_csrf_token
    print("Token from db: ", x_csrf_token )

    headers['x-csrf-token'] =  x_csrf_token


    json_data = {
                "format_currency": True,
                "id": x_yataxi_userid,      
                "orderid": order_info.yandex_order_id
                }
    async with session.post(url, json = json_data, cookies=cookies, headers=headers,) as response:
        order = await response.text()
        print("-> Status of order with id %s" % order_info.yandex_order_id)
        # print("Result ", order)

        status_code = response.status


        if status_code == 401:
            print("Unauthorized 401")

        if status_code == 404:
            print("Order not found")    
        if status_code == 200:  
            response = json.loads(order)
            handle_driver_object(response,order_info)

        return response


async def get_orders_status(orders):

    async with aiohttp.ClientSession() as session:

        tasks = []

        for info in orders:
            tasks.append(asyncio.ensure_future(get_order(session,info)))

        await asyncio.gather(*tasks)

from sqlalchemy import and_, or_, not_

# get order ids with status search_car from db
def get_active_orders():
     ids = []
     db = get_db()
     orders = next(db).query(models.Order).filter(or_(
                                                        models.Order.status == "search_car",
                                                        models.Order.status == "assigned")).all()
     for order in orders:
         print(order.status)
         if order.yandex_order_id != None:
            ids.append(OrderInfo(order.yandex_order_id,order.status,order.order_id,order.fb_token))

     return ids    

from app.fb_helper import send_push_notification

def handle_driver_object(response,order_info):

            print("USER STATUS: ",order_info.status)
            print("СТАТУС ПОИСКА: ",response["status"])
            status = response["status"]

            if status == "search":
                print("Идет поиск машины: " )
            if status == "assigned":
                print("Yandex Driver Assigned")
    
            if status == "driving" or status == "waiting" or status == "transporting":
                driver = response["driver"] 
                driver_name = driver['name']
                car_color = driver['color']
                car_model = driver['model']
                plates = driver['plates']
                price = str(response['final_cost'])
                rating = driver['rating']
                phone_num = str(driver['forwarding']['phone'])
                print("К Вам выехал " , car_color, ' ', car_color , ',  гос номер:' ,plates )
                print("О водителе: " , driver_name, ',', phone_num )
                print("Водитель назначен: ", driver)
                car_info = str(car_color) +' ' +str(car_model) +' ' + str(plates)
                driver_info = DriverInfo(full_name = driver_name,car_info=car_info,phone_num=phone_num,final_cost=price)
                # send message to client
                if status == "driving":
                    driver_lat = driver['car'][1]
                    driver_lng = driver['car'][0]


                    print("DRIVER Coordinates", driver_lat)

                    # update driver position
                    update_order_driver_lat_lng(order_info.order_id,driver_lat,driver_lng)


                    if order_info.status != "assigned":
                        # update_order_status(order_info.yandex_order_id,"assigned")
                        driver_info.title = "💁 - К вам выехала машина."
                        update_order_status_in_db_and_fb(order_info.order_id,driver_info,"assigned")
                        send_push_notification(order_info.fb_token,"💁 - К вам выехала машина.",car_info)
                        
                if status == "waiting":
         
                    # update_order_status(order_info.yandex_order_id,"driver_wait")
                    driver_info.title = "💁 *- Водитель подьехал. Вас ожидает:*\n\n*"
                    update_order_status_in_db_and_fb(order_info.order_id,driver_info,"arrived")
                    send_push_notification(order_info.fb_token,"💁 Водитель подьехал. Вас ожидает:",car_info)

    
            if status == "cancelled":
                print("Заказ отменен клиентом: ")  
            if status == "expired":
                print("Машина не найдена")
                send_push_notification(order_info.fb_token,"💁 К сожалению машина не найдена!",car_info)
                driver_not_found_info_in_db_and_fb(order_info.order_id)  

                
                     

def run_get_status_def():
    while True :
        start_time = time.time()
        orders = get_active_orders()
        if len(orders) > 0:
            print(start_time)
            asyncio.run(get_orders_status(orders))
            
        else:
            print("Not active orders for listening")
        print("--- %s seconds ---" % (time.time() - start_time))    
        time.sleep(10)

# start_time = time.time()
# asyncio.run(get_orders_status())
# print("--- %s seconds ---" % (time.time() - start_time))

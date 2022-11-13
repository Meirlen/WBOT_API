# import requests
# import time
# import datetime
# from yandex.json_data import *
# import json



# def get_order(order_id, cancel = False):


#     json_data = {
#                 "format_currency": True,
#                 "id": x_yataxi_userid,      
#                 "orderid": order_id
#                 }

#     if cancel:
#        json_data["break"] = "user"            

#     response = requests.post('https://pokeapi.co/api/v2/pokemon/', cookies=cookies, headers=headers,
#                              json=json_data)

#     # text = json.loads(response.text)

#     print(response.status_code)



# async def get_pokemon(session, url):
#     async with session.get(url) as resp:
#         pokemon = await resp.json()
#         return pokemon['name']

    
# def start_listening():
#     while True :

#         print("get request")

#         searh_car_status_orders_ids = ['a','b','c','d','e','j','k','l','m','n','o']

#         if len(searh_car_status_orders_ids) > 0:
#             start_time = time.time()

#             for order_id in searh_car_status_orders_ids:
#                 print('request: ' , order_id) 
#                 get_order(order_id)

#             print("--- %s seconds ---" % (time.time() - start_time))



#         time.sleep(10)
#         # get_order("dfc0160863cdc4febd3add5e742b74b6")

from dataclasses import dataclass

@dataclass
class OrderInfo:
    yandex_order_id:str
    user_id: str  
    status:str



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
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas as schemas
from app.wati_msg_builder import *
import os


def get_saved_last_token():
     db = get_db()
     csrf_token = next(db).query(models.Credentials).filter(models.Credentials.name == "csrf_token").first()
     return csrf_token.value   


async def get_order(session, order_info:OrderInfo):

    url = 'https://ya-authproxy.taxi.yandex.ru/3.0/taxiontheway'


    # set csrf token
    x_csrf_token = os.getenv("CSRF_TOKEN",None)

    if x_csrf_token == None:
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
            ids.append(OrderInfo(order.yandex_order_id,order.user_id,order.status))

     return ids    


def update_order_status(yandex_order_id,new_status):
    db = next(get_db())
    order_query = db.query(models.Order).filter(models.Order.yandex_order_id == yandex_order_id)
    order_query.update({"status":new_status}, synchronize_session=False)    
    db.commit()



def send_driver_assigned_info_to_whatsapp(user_id,driver_info:DriverInfo,status):
    db = next(get_db())
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        print('error')
    else:
        phone_number = user.phone_number
        send_driver_assigned_info(phone_number,driver_info)

        order = db.query(models.Order).filter(models.Order.user_id == user.id).order_by(models.Order.order_id.desc()).first() 


        order_query = db.query(models.Order).filter(models.Order.order_id == order.order_id)
        order_query.update({"status":status}, synchronize_session=False)    
        db.commit()


def send_driver_not_found_info_to_whatsapp(user_id):
    db = next(get_db())
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
       print('error')
    else:
       phone_number = user.phone_number
       send_driver_not_found(phone_number) 


def handle_driver_object(response,order_info):

        
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
                    if order_info.status != "assigned":
                        # update_order_status(order_info.yandex_order_id,"assigned")
                        driver_info.title = "💁 *- К вам выехала машина.*\n\n*"
                        send_driver_assigned_info_to_whatsapp(order_info.user_id,driver_info,"assigned")
                if status == "waiting":
                    # update_order_status(order_info.yandex_order_id,"driver_wait")
                    driver_info.title = "💁 *- Водитель подьехал. Вас ожидает:*\n\n*"
                    send_driver_assigned_info_to_whatsapp(order_info.user_id,driver_info,"arrived")

    
            if status == "cancelled":
                print("Заказ отменен клиентом: ")  
            if status == "expired":
                print("Машина не найдена")
                update_order_status(order_info.yandex_order_id,"expired")
                send_driver_not_found_info_to_whatsapp(order_info.user_id)  

                
                     

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

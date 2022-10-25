from tkinter.messagebox import NO
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from app.wati_msg_builder import *
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas as schemas
from .. import oauth2
from app.database import get_db
from yandex.create_order import *
from yandex.active_order import *
router = APIRouter(
    prefix="/webhook",
    tags=['Whatsapp']
)
    
   
@router.post("/message", status_code=status.HTTP_200_OK)
async def whatsapp_input(input_message: schemas.WhatsappMessage,background_tasks: BackgroundTasks, db: Session = Depends(get_db),):

    print(input_message)

    # # hash the password - user.password
    # hashed_password = utils.hash(user.password)
    # user.password = hashed_password
    user_message = input_message.text
    phone_number = input_message.waId
    user_name = input_message.senderName
    user = db.query(models.User).filter(models.User.phone_number == phone_number).first()
    user_id = str(user.id)

    if not user:
        # Registr whatsapp user
        print("User send message at first time, need to add in user table")
        new_user = models.User(phone_number = phone_number, role="wuser",user_name = user_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # send message to whatsapp async
        background_tasks.add_task(send_greet_message,phone_number,user_name,user_id)
        
    else:
        print("User already exist: ", user.user_name)

        order = db.query(models.Order).filter(models.Order.user_id == user.id,models.Order.status != "cancel_by_user").first()
        if not order:
            print("The user dont't have  any order proccess")
            send_template_ask_fill_address(phone_number,user_id)
        else:    

            order_status =  order.status
            order_query = db.query(models.Order).filter(models.Order.order_id == order.order_id)

            if order_status == "open":
                # Принятие заказа
                if "Эконом" in user_message:

                    send_car_search_info(phone_number)                          
                    # Update Postgres order table
                    order_query.update({"status":"search_car"}, synchronize_session=False)    
                    db.commit()

                    
                    # Create order in Yandex using yandex api START
                    routes = db.query(models.Route).filter(models.Route.order_id == order.order_id)

                    route_array = []
                    for route in routes:
                        route_array.append({
                                                "short_text": route.short_text,
                                                "geopoint": [
                                                    route.lat,
                                                    route.lng,
                                                ],
                                                "fullname": route.fullname,
                                                "type": route.type,
                                                "city":  route.city
                                            })
                    
                    yandex_order_id = create_draft(route_array)

                    if yandex_order_id != None:
                        # Update Postgres order table
                        order_query.update({"yandex_order_id":yandex_order_id}, synchronize_session=False)    
                        db.commit()
                    # Create order in Yandex using yandex api FINISH






                # else:
                #    send_price_info(phone_number) 

            elif order_status == "search_car":

                if user_message == CANCEL_BTN_TITLE:
                    # Cancel order by user in Yandex using yandex api START
                    print("Клиент отменил заказ")
                    send_message(phone_number, '💁 *- Заказ отменен.*')                          
                    # Update Postgres order table
                    order_query.update({"status":"cancel_by_user"}, synchronize_session=False)    
                    db.commit()

                    send_template_ask_fill_address(phone_number,user_id)

                    # Cancel order in Yandex using yandex api START
                    yandex_order_id = order.yandex_order_id
                    get_order(yandex_order_id,True)
                    print("YORDER_ID ",yandex_order_id)


                else:   
                   send_car_search_info(phone_number)

            elif order_status == "assigned":
                 send_car_search_info(phone_number)     
            else:
                print('csdc')
            



    return input_message    
  






import aiohttp
import asyncio

API_YANDEX_URL = 'https://suggest-maps.yandex.ru/suggest-geo?apikey=a4018892-4411-4709-97ea-6881ac674715&v=7&search_type=all&lang=ru_RU&n=50&bbox=72.958828,49.730972~73.267132,49.989920&part=';



# async def suggest(query):

#     async with aiohttp.ClientSession() as session:

#         async with session.get(API_YANDEX_URL+query) as resp:
#             response = await resp.text()
#             response = response.replace("suggest.apply(",'')
#             # response = response[0,-1]
#             print(response)
#             return response

# # asyncio.run(suggest("Наза"))

import json

def suggest(query):


    response = requests.get(API_YANDEX_URL+query)
    response = response.text.replace("suggest.apply(",'')[:-1]
    json_object = json.loads(response)

    # text = json.loads(response.text)

    return json_object


@router.get("/get_suggest", )
async def get_orders(q,response: Response):
    response.headers['Access-Control-Allow-Origin'] = '*'


   
    return suggest(q)


   
     
  
    
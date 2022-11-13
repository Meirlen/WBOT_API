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
from datetime import datetime, timezone
from admin.telegram_api import *

router = APIRouter(
    prefix="/webhook",
    tags=['Whatsapp']
)
from sqlalchemy import and_, or_, not_
    
   
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

    if not user:
        # Registr whatsapp user
        print("User send message at first time, need to add in user table")
        new_user = models.User(phone_number = phone_number, role="wuser",user_name = user_name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # send message to whatsapp async
        background_tasks.add_task(send_greet_message,phone_number,user_name,str(new_user.id))
        
    else:
        print("User already exist: ", user.user_name)
        user_id = str(user.id)

        # order = db.query(models.Order).filter(models.Order.user_id == user.id,and_(
        #     models.Order.status != "cancel_by_user",models.Order.status != "expired"),).first()

        # get last order by ORDER DESC
        order = db.query(models.Order).filter(models.Order.user_id == user.id).order_by(models.Order.order_id.desc()).first() 


        if not order:
            print("The user dont't have  any order proccess")
            send_template_ask_fill_address(phone_number,user_id)
            return input_message


        print("Order id", order.order_id)    
        curr_time = datetime.now(timezone.utc)
        order_time = order.created_at
        difference =  curr_time - order_time
        duration_in_s = difference.total_seconds()
        minutes = divmod(duration_in_s, 60)[0]   
        print("Order created ", minutes , " min ago")

        if not order or minutes > 120:
            print("The user dont't have  any order proccess")
            send_template_ask_fill_address(phone_number,user_id)
        else:    

            order_status =  order.status
            order_query = db.query(models.Order).filter(models.Order.order_id == order.order_id)

       
    
            if order_status == "search_car":
                if user_message == CANCEL_BTN_TITLE:
                    cancel_order_by_user(phone_number, user_id,order_query,db,order)
                else:   
                   send_car_search_info(phone_number)


            elif order_status == "assigned":
                if user_message == CANCEL_BTN_TITLE:
                    cancel_order_by_user(phone_number, user_id,order_query,db,order)
                else:   
                    sended_car_info(phone_number,'💁 *- Ожидайте авто, к вам уже выехала машина*\n\n') 

            elif order_status == "arrived":
                if user_message == CANCEL_BTN_TITLE:
                    cancel_order_by_user(phone_number, user_id,order_query,db,order)
                else:   
                    sended_car_info(phone_number,'💁 *- Машина ожидает вас, выходите!*\n\n') 
            else:
                print(order_status)
                send_template_ask_fill_address(phone_number,user_id)




    return input_message    
  

def cancel_order_by_user(phone_number, user_id,order_query,db,order):
    print("Клиент отменил заказ")
    send_message(phone_number, '💁 *- Заказ отменен.*')                          
    # Update Postgres order table
    order_query.update({"status":"cancel_by_user"}, synchronize_session=False)    
    db.commit()

    send_template_ask_fill_address(phone_number,user_id)


    send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ КЛИЕНТ ОМЕНИЛ ЗАКАЗ! \n ' + str(phone_number) )               

    

    yandex_order_id = order.yandex_order_id
    if yandex_order_id != None:
        # Cancel order by user in Yandex using yandex 
        get_order(yandex_order_id,True) 
        print("YORDER_ID  ",yandex_order_id)




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



import os

@router.get("/get_yandex_token", )
async def get_y_token(response: Response):
    response.headers['Access-Control-Allow-Origin'] = '*'


   
    return os.getenv("CSRF_TOKEN",None)  


@router.post("/yandex_token_update", )
async def set_y_token(upd: schemas.UpdateYToken, db: Session = Depends(get_db)):   
    os.environ["CSRF_TOKEN"] = upd.token
    cred = db.query(models.Credentials).filter(models.Credentials.name == "csrf_token")
    cred.update({"value":str(upd.token)}, synchronize_session=False)    
    db.commit()

    return {"response": upd.token}    
    
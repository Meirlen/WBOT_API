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
async def whatsapp_input(input_message: schemas.WhatsappMessage,response: Response,background_tasks: BackgroundTasks, db: Session = Depends(get_db),):


    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Auth-Token'
    
    print(input_message)
    user_id = input_message.user_id
    if user_id != None:
         user = db.query(models.User).filter(models.User.id == user_id).first()
         input_message.waId = user.phone_number
         input_message.senderName= user.user_name
    else:
         input_message.waId =  "7"+input_message.waId[1:]

    user_message = input_message.text
    phone_number = input_message.waId
    user_name = input_message.senderName
    type_msg = input_message.type
    link_data = input_message.data

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
        return input_message    

    else:
        print("User already exist: ", user.user_name)
        user_id = str(user.id)

        driver = db.query(models.Driver).filter(models.Driver.user_id == user.id).first()
        driver_templates = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number).first()
        if driver != None :
            print("Driver already registered")
            return input_message

        if driver_templates == None:
            background_tasks.add_task(send_greet_message,phone_number,user_name)
            print("Driver send message at first time, need to add in driver templates table")
            new_driver = models.DriverTemplates(phone = phone_number)
            db.add(new_driver)
            db.commit()
            db.refresh(new_driver)
            return input_message    

        else:

            driver_name = driver_templates.driver_name
            d_pasport_photo_1 = driver_templates.d_pasport_photo_1
            d_pasport_photo_2 = driver_templates.d_pasport_photo_2
            d_pasport_photo_3 = driver_templates.d_pasport_photo_3
            car_model= driver_templates.car_model
            car_number = driver_templates.car_number
            car_year= driver_templates.car_year
            car_body= driver_templates.car_body
            car_color= driver_templates.car_color


            car_pasport_photo_1 = driver_templates.car_pasport_photo_1
            car_pasport_photo_2 = driver_templates.car_pasport_photo_2

            car_photo = driver_templates.car_photo
            user_photo = driver_templates.user_photo

            if driver_name == None:
                driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                driver_templates_query.update({"driver_name":user_message}, synchronize_session=False)    
                db.commit()
                background_tasks.add_task(send_ask_driver_pasport,phone_number)
                return input_message

            if d_pasport_photo_1 == None:

                if str(type_msg) == "image":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"d_pasport_photo_1":link_data}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_driver_pasport2,phone_number)
                    return input_message
                else:  
                    
                    background_tasks.add_task(send_ask_driver_pasport,phone_number)
                    return input_message 


            if d_pasport_photo_2 == None:

                if str(type_msg) == "image":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"d_pasport_photo_2":link_data}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_driver_pasport3,phone_number)
                    return input_message
                else:  
                    
                    background_tasks.add_task(send_ask_driver_pasport2,phone_number)
                    return input_message  


            if d_pasport_photo_3 == None:

                if str(type_msg) == "image":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"d_pasport_photo_3":link_data}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_car_info,phone_number)
                    return input_message
                else:  
                    background_tasks.add_task(send_ask_driver_pasport3,phone_number)
                    return input_message  


 
            if car_model == None:
                if str(type_msg) == "text":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"car_model":user_message}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_car_info2,phone_number)
                    return input_message
                else:  
                    background_tasks.add_task(send_ask_car_info,phone_number)
                    return input_message  



            if car_number == None:
                if str(type_msg) == "text":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"car_number":user_message}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_car_info2_1,phone_number)
                    return input_message
                else:  
                    background_tasks.add_task(send_ask_car_info2,phone_number)
                    return input_message  



            if car_color == None:
                    if str(type_msg) == "text":
                        driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                        driver_templates_query.update({"car_color":user_message}, synchronize_session=False)    
                        db.commit()
                        background_tasks.add_task(send_ask_car_info2_2,phone_number)
                        return input_message
                    else:  
                        background_tasks.add_task(send_ask_car_info2_1,phone_number)
                        return input_message  

            

            if car_year == None:
                    if str(type_msg) == "text":
                        driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                        driver_templates_query.update({"car_year":user_message}, synchronize_session=False)    
                        db.commit()
                        background_tasks.add_task(send_ask_car_info2_3,phone_number)
                        return input_message
                    else:  
                        background_tasks.add_task(send_ask_car_info2_2,phone_number)
                        return input_message   
                        
            if car_body == None:
                    if str(type_msg) == "text":
                        driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                        driver_templates_query.update({"car_body":user_message}, synchronize_session=False)    
                        db.commit()
                        background_tasks.add_task(send_ask_car_info3,phone_number)
                        return input_message
                    else:  
                        background_tasks.add_task(send_ask_car_info2_3,phone_number)
                        return input_message   


            if car_pasport_photo_1 == None:

                if str(type_msg) == "image":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"car_pasport_photo_1":link_data}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_car_info4,phone_number)
                    return input_message
                else:  
                    
                    background_tasks.add_task(send_ask_car_info3,phone_number)
                    return input_message 



            if car_pasport_photo_2 == None:

                if str(type_msg) == "image":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"car_pasport_photo_2":link_data}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_car_info5,phone_number)
                    return input_message
                else:   
                    
                    background_tasks.add_task(send_ask_car_info4,phone_number)
                    return input_message 


            if car_photo == None:

                if str(type_msg) == "image":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"car_photo":link_data}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_ask_profile_1,phone_number)
                    return input_message
                else:   
                    
                    background_tasks.add_task(send_ask_car_info5,phone_number)
                    return input_message 

            if user_photo == None:

                if str(type_msg) == "image":
                    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == phone_number)
                    driver_templates_query.update({"user_photo":link_data}, synchronize_session=False)    
                    db.commit()
                    background_tasks.add_task(send_reg_completed,phone_number)
                    return input_message
                else:   
                    
                    background_tasks.add_task(send_ask_car_info5,phone_number)
                    return input_message 


    background_tasks.add_task(send_reg_completed,phone_number)
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
    
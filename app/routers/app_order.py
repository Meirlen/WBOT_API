from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas as schemas,oauth2
from ..database import get_db

from app.wati_msg_builder import *
from yandex.calc_price import *
from baursak.calc_b_price import *
from region.calc_region_price import *
from yandex.create_order import *
from admin.telegram_api import *
from alem.calc_alem_price import get_price_by_route_alem

from app.fb_helper import create_order_in_firebase,change_order_status,update_order_status_in_firebase,send_push_notification_to_multiple_devices


router = APIRouter(
    prefix="/mobile/order",
    tags=['Orders']
)



@router.get("/", )
def get_orders(db: Session = Depends(get_db)):
   
    orders = db.query(models.Order).all()
       
    return {"data": orders}


def send_push_to_active_drivers(db,from_address):
   

    query = "SELECT users.fb_token FROM users INNER JOIN drivers ON users.id=drivers.user_id WHERE drivers.is_online = 0 AND users.fb_token IS NOT NULL ;"
    orders_query = db.execute(query)
    fb_tokens = orders_query.all()
    registration_ids = []
    for token in fb_tokens:
        registration_ids.append(token.fb_token)

    if len(registration_ids)>0:
       send_push_notification_to_multiple_devices(registration_ids,"⚡🥳 Sapar, поступил заказ!",from_address)
 


       

@router.get("/bonus_count", )
def get_bonus_count(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
   
    user_id = current_user.id
    query = "SELECT * FROM orders WHERE user_id = '"+str(user_id)+"' ORDER BY order_id DESC"
    orders_query = db.execute(query)

    bounus_info = 0
    for row in  orders_query :
        app_type = row['app_type']
        if app_type == "a" and row['price']!=None:
           bonus = int(row['price'])/100
           bounus_info = bounus_info+int(bonus)



    return {"bonus_count": bounus_info}



@router.get("/history", )
def get_orders_history(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id

       # get last order of user if order status == 'assigned','arrived','search_car'
    query = "SELECT * FROM orders WHERE user_id = '"+str(user_id)+"' ORDER BY order_id DESC"
    # query = "SELECT * FROM orders INNER JOIN routes ON orders.order_id=routes.order_id;"
    orders_query = db.execute(query)

    orders = []
    bounus_info = None
    for row in  orders_query :
        bounus_info = None
        routes = db.query(models.Route).filter(models.Route.order_id == row['order_id']).all()
        app_type = row['app_type']
        if app_type == "a" and row['price']!=None:
           bonus = int(row['price'])/100
           bounus_info = int(bonus)
        

        orders.append({"order_info":row, "route":routes, "bounus_info":bounus_info})


    # orders = db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.order_id.desc()).all()
       
    return {"orders": orders}    


def create_yandex_order(db,order_id,routes,client_phone_number):

    order_query = db.query(models.Order).filter(models.Order.order_id == order_id)
    yandex_order_id = send_order_to_yandex(routes,client_phone_number)
    print("YANDEX ORDER ID", yandex_order_id)

    if yandex_order_id != None:
        # Update Postgres order table
        order_query.update({"yandex_order_id":yandex_order_id}, synchronize_session=False)    
        db.commit()







@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order( order: schemas.UserOrderCreate,
                        response: Response,
                        background_tasks: BackgroundTasks,
                        db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Auth-Token'
    # response.headers['Access-Control-Allow-Origin'] = 'http://165.22.13.172'

    # create new order
    user = current_user
    user_id = current_user.id
    user_fb_token = current_user.fb_token


    # add to local db
    new_order = models.Order(user_id = user_id,app_type = order.app_type,tariff = order.tariff,fb_token = user_fb_token)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # add to firebase
    
    print("\nUSER CREATED ORDER , user_phone", str(user.phone_number) )

    fb_routes = []
    for route in order.route:
        fb_routes.append(
            {
                "short_text":route.short_text,
                "fullname":route.fullname,
                "lat":route.geo_point[0],
                "lng":route.geo_point[1]},
            )




    order_id = new_order.order_id
 

    # create new route
    routes = order.route
    route_array = []
    for route in routes:
        new_route = models.Route(   short_text = route.short_text,
                                    fullname = route.fullname,
                                    lat = round(route.geo_point[0], 6),
                                    lng =  round(route.geo_point[1], 6),
                                    type = route.type,
                                    city = route.city,
                                    order_id = new_order.order_id )

        route_array.append([route.geo_point[1],route.geo_point[0]])

        db.add(new_route)
        db.commit()
        db.refresh(new_route)

    # calculate orders

    app_type = order.app_type
    tariff= order.tariff

    comment= order.comment
    if comment == "":
       comment = None 

    price_info = None
    price = None
    aggregator = None
    if tariff == "e":
        tariff = "Эконом"
    if tariff == "c":
            tariff = "Комфорт"     

    if app_type == "y":
        price_info = get_price_by_route(route_array)
        aggregator = "Яндекс"
        phone_number = user.phone_number.replace('7', '8', 1)
        print("User phone num ", phone_number)
        create_yandex_order(db,order_id,routes,phone_number)

    if app_type == "r":
        print("Region arr ", route_array)
        price_info =  get_price_by_route_region(route_array)
        aggregator = "Регион"

    if app_type == "b":
        price_info = get_price_by_route_baursak(route_array)
        aggregator = "Бауырсак"

    if app_type == "a":
        price_info = get_price_by_route_alem(route_array)
        aggregator = "Алем"    

    if app_type == "j":
       price_info = order.tariff
       aggregator = "Jol KZ"
    
  


    # PRICE INFO
    print("Price info", str(price_info))
    if  price_info != None:
            if app_type == "a":
                price = price_info[0]['price']

            else:    
                if len(price_info) > 1:
                    if order.tariff == "e":
                        price = price_info[1]['price']
                    if order.tariff == "c":
                        price = price_info[0]['price']  
                else:
                    price = "0"        


    background_tasks.add_task(create_order_in_firebase,
        new_order.order_id,
        str(price),
        fb_routes,
        new_order.created_at)


    order_query = db.query(models.Order).filter(models.Order.order_id == order_id)
    order_query.update({"price":price}, synchronize_session=False)    
    db.commit()



    
 



    # send to telegram admin user order created message
    if user:
        from_address = order.route[0].short_text


   


        to_address_array = order.route[1:]
        if len(to_address_array) == 1:
            to_address =  order.route[1].short_text
        else:    
            to_address =  ""
            for address in to_address_array:
                to_address = to_address + " "+ address.short_text + ", "

        print("USER PHONE NUMBER: ", user.phone_number)        
        address = from_address + "  \n"+ to_address

             # send push message to active drivers
        send_push_to_active_drivers(db,from_address + " ➡️ "+  to_address)
        send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ Поступил НОВЫЙ ЗАКАЗ! \n '+ aggregator +  " \n "+ str(user.phone_number)+"\n"+address+"\n Комментарий: "+str(comment))               

    return {"order_id": order_id, "app_type": app_type}









from datetime import datetime, timezone

def calculate_order_created_time_in_minutes(created_at):
    curr_time = datetime.now(timezone.utc)
    order_time = created_at
    difference =  curr_time - order_time
    duration_in_s = difference.total_seconds()
    minutes = divmod(duration_in_s, 60)[0]   
    return minutes

@router.get('/active_order', status_code=status.HTTP_200_OK)
def get_user_last_order_status(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):

    user = current_user
    if user == None:
        return {
                   "order": None,
                   "routes":None,
                   "driver":None,

                   }

    user_id = current_user.id
               
    # get last order by ORDER DESC
    order = db.query(models.Order).filter(models.Order.user_id == user_id).order_by(models.Order.order_id.desc()).first() 
    if not order:
            print("The user dont't have  any order proccess")
            return {
                   "order": None,
                   "routes":None,
                   "driver":None,

                   }
    

    after_created_min = calculate_order_created_time_in_minutes(order.created_at)
    print("Order created ", after_created_min , " min ago")

    if not order or after_created_min > 120:
        print("The user dont't have  any order proccess")
        return {   "order": None,
                   "routes":None,
                   "driver":None,}


    elif  order.status == "arrived" and after_created_min > 5:
        return {   "order": None,
                   "routes":None,
                   "driver":None,}               
    else: 
        order_status =  order.status
        if order_status == "search_car" or  order_status == "assigned" or order_status == "arrived":

            routes = db.query(models.Route).filter(models.Route.order_id == order.order_id).all()


            driver = None

            if order_status == "assigned" or order_status == "arrived":
                driver = db.query(models.Driver).filter(models.Driver.order_id == order.order_id).order_by(models.Driver.order_id.desc()).first()

            return {
                    
                    "order":order,
                    "routes":routes,
                    "driver":driver
            }
        else:
            return { 
                   "order": None,
                   "routes":None,
                   "driver":None,}   

    
@router.post("/estimate", status_code=status.HTTP_200_OK)
async def create_draft(order: schemas.OrderEstimate,response: Response,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    routes = order.route
    route_array = []
    route_name_array = []

    for route in routes:
        lat_point = round(route.geo_point[1], 6)
        lon_point = round(route.geo_point[0], 6)

        route_array.append([lat_point,lon_point])
        route_name_array.append(route.short_text)


    print("\nCLIENT REQUEST ESTIMATE , route: ", str(route_name_array))
    # if yandex_price_info == None:
    # yandex_price_info = get_price_by_route(route_array)
    yandex_price_info =   get_price_by_route(route_array)
    baursak_price_info = get_price_by_route_baursak(route_array)
    region_price_info = get_price_by_route_region(route_array)
    alem_price_info = get_price_by_route_alem(route_array)


    print(route_array)


    response =  {
         "yandex":yandex_price_info,
         "baursak": baursak_price_info,
         "region": region_price_info,
         "alem": alem_price_info,

    }

    # print(response)

    
    return response




@router.post("/update_status", status_code=status.HTTP_200_OK)
async def update_status(order: schemas.OrderStatus,db: Session = Depends(get_db)):
   
    
    # get last order by ORDER DESC
    # change order status to Assigned 
    order_query = db.query(models.Order).filter(models.Order.order_id == order.order_id)
    order_query.update({"status":order.status}, synchronize_session=False)    
    db.commit()

    if order.status == "cancel_by_user":
        update_order_status_in_firebase(order.order_id,order.status)
        send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ КЛИЕНТ ОМЕНИЛ ЗАКАЗ! \n ' + str(order.order_id) )  


    


    return {"order_id": order.order_id, "status": order.status}






# Require no auto taxi like Region,Baursak
@router.post("/send_driver_assigned_info", status_code=status.HTTP_200_OK)
async def send_driver_info(driver_info_params: schemas.OrderDriverInfo,db: Session = Depends(get_db)):
   
    driver_info = DriverInfo(   
                                full_name = driver_info_params.driver_name,
                                car_info=driver_info_params.car_info,
                                phone_num=driver_info_params.user_phone,
                                final_cost=driver_info_params.price
                            )


    status = driver_info_params.status

    if status == "assigned":
       driver_info.title = "💁 *- К вам выехала машина.*\n\n*"

    if status == "arrived":
       driver_info.title = "💁 *- Вас ожидает такси.*\n\n*"    

    user = db.query(models.User).filter(models.User.phone_number == driver_info_params.user_phone).first()  
    order = db.query(models.Order).filter(models.Order.user_id == user.id).order_by(models.Order.order_id.desc()).first()
    order_id = order.order_id




    send_driver_assigned_info(driver_info_params.user_phone,driver_info)


    order_query = db.query(models.Order).filter(models.Order.order_id == order_id)
    order_query.update({"status":status}, synchronize_session=False)    
    db.commit()


    return {"order_id": order_id, "status": status}







from yandex.yandex_geo_coder import *

@router.post("/geocode", status_code=status.HTTP_200_OK)
async def geocode(request: schemas.GeoCodeRequest,db: Session = Depends(get_db)):
   
    address = get_address_by_coords(request.lon,request.lat)


    return  {
            "text": address
    }    
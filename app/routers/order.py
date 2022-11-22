from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas as schemas
from ..database import get_db

from app.wati_msg_builder import *
from yandex.calc_price import *
from baursak.calc_b_price import *
from region.calc_region_price import *
from yandex.create_order import *
from admin.telegram_api import *

router = APIRouter(
    prefix="/order",
    tags=['Orders']
)



@router.get("/", )
def get_orders(db: Session = Depends(get_db)):
   
    orders = db.query(models.Order).all()
       
    return {"data": orders}


def create_yandex_order(db,order_id,routes,client_phone_number):

    order_query = db.query(models.Order).filter(models.Order.order_id == order_id)
    yandex_order_id = send_order_to_yandex(routes,client_phone_number)
    print("YANDEX ORDER ID", yandex_order_id)

    if yandex_order_id != None:
        # Update Postgres order table
        order_query.update({"yandex_order_id":yandex_order_id}, synchronize_session=False)    
        db.commit()



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderCreate,response: Response,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Content-Type, X-Auth-Token'
    # response.headers['Access-Control-Allow-Origin'] = 'http://165.22.13.172'

    # create new order
    new_order = models.Order(user_id = order.user_id,app_type = order.app_type,tariff = order.tariff)
    user = db.query(models.User).filter(models.User.id == order.user_id).first()

    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


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

        route_array.append([route.geo_point[0],route.geo_point[1]])

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
    aggregator = None
    if tariff == "e":
        tariff = "Эконом"
    if tariff == "c":
            tariff = "Комфорт"     
    price = None

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
    
  

    if  price_info != None:
            if order.tariff == "e":
                price = price_info[1]['price']
            if order.tariff == "c":
                price = price_info[0]['price']    
    if user:
        # send to whatsapp user order created message

        from_address = order.route[0].short_text

        to_address_array = order.route[1:]
        if len(to_address_array) == 1:
            to_address =  order.route[1].short_text
        else:    
            to_address =  ""
            for address in to_address_array:
                to_address = to_address + " "+ address.short_text + ", "

        print("USER PHONE NUMBER: ", user.phone_number)        

        send_order_info(
                        user.phone_number,
                        from_address,
                        to_address,
                        aggregator,
                        tariff,
                        price,
                        comment)

        address = from_address + "  \n"+ to_address
        send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ Поступил НОВЫЙ ЗАКАЗ! \n '+ aggregator +  " \n "+ str(user.phone_number)+"\n"+address+"\n Комментарий: "+str(comment))               

    return {"order_id": order_id, "app_type": app_type}


    # print("Order created in Postgres")
    # # background_tasks.add_task(create_order_in_firebase,
    # #     new_order.order_id,
    # #     order.from_address,
    # #     order.to_address,
    # #     order.price,
    # #     order.from_lat,
    # #     order.from_lng,
    # #     order.to_lat,
    # #     order.to_lng)
    # user = db.query(models.User).filter(models.User.id == order.user_id).first()
    # if user:
    #    send_price_info(user.phone_number) 





        
    return new_order

    
@router.post("/estimate", status_code=status.HTTP_201_CREATED)
async def create_draft(order: schemas.OrderEstimate,response: Response,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    routes = order.route
    route_array = []
    for route in routes:
        lat_point = round(route.geo_point[1], 6)
        lon_point = round(route.geo_point[0], 6)

        route_array.append([lat_point,lon_point])

    # if yandex_price_info == None:
    # yandex_price_info = get_price_by_route(route_array)
    yandex_price_info =   get_price_by_route(route_array)
    baursak_price_info = get_price_by_route_baursak(route_array)
    region_price_info = get_price_by_route_region(route_array)


    print(route_array)

    
    return  {
         "yandex":yandex_price_info,
         "baursak": baursak_price_info,
         "region": region_price_info

    }




@router.post("/update_status", status_code=status.HTTP_200_OK)
async def update_status(order: schemas.OrderStatus,db: Session = Depends(get_db)):
   
    
    # get last order by ORDER DESC
    # change order status to Assigned 
    order_query = db.query(models.Order).filter(models.Order.order_id == order.order_id)
    order_query.update({"status":"assigned"}, synchronize_session=False)    
    db.commit()


    return {"order_id": order.order_id, "status": order.status}


@router.post("/driver_location", status_code=status.HTTP_200_OK)
async def get_driver_location(request: schemas.DriverLocation,db: Session = Depends(get_db)):
   
    
    # get last order by ORDER DESC
    # change order status to Assigned 
    order = db.query(models.Order).filter(models.Order.order_id == request.order_id).first()


    return  {
            "lat":order.d_lat,
            "lng":order.d_lng
    }




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
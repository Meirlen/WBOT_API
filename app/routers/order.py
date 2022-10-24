from unittest import result
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas as schemas
from ..database import get_db

from ..wati_msg_builder import *
from yandex.calc_price import *
router = APIRouter(
    prefix="/order",
    tags=['Orders']
)



@router.get("/", )
def get_orders(db: Session = Depends(get_db)):
   
    orders = db.query(models.Order).all()
       
    return {"data": orders}




@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: schemas.OrderCreate,background_tasks: BackgroundTasks, db: Session = Depends(get_db)):


    # create new order
    new_order = models.Order(user_id = order.user_id)
    user = db.query(models.User).filter(models.User.id == order.user_id).first()

    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)


    order_id = new_order.order_id
    # send to whatsapp user order created message
    if user:
        send_order_info(user.phone_number,order.route[0].short_text,order.route[1].short_text)

    # create new route
    routes = order.route
    route_array = []
    for route in routes:
        
        new_route = models.Route(   short_text = route.short_text,
                                    fullname = route.fullname,
                                    lat = route.geo_point[0],
                                    lng = route.geo_point[1],
                                    type = route.type,
                                    city = route.city,
                                    order_id = new_order.order_id )

        route_array.append([route.geo_point[0],route.geo_point[1]])

        db.add(new_route)
        db.commit()
        db.refresh(new_route)

    # calculate orders
  
    price_info = get_price_by_route(route_array)
    if price_info == None:
        return {"order_id": order_id}
    else:
        
        # send to whatsapp user message with prices
        if user:
            yandex_econom = price_info[0]['name_tariff'] + "-" + price_info[0]['price']
            yandex_bussines = price_info[1]['name_tariff'] + "-" + price_info[1]['price']
            send_price_info(user.phone_number,yandex_econom,yandex_bussines) 

        return {
            
               "order_id": order_id,
               "price_yandex": price_info
               
               }






    


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

    

  


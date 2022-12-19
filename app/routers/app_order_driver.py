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

from app.fb_helper import create_order_in_firebase,change_order_status,update_order_status_in_firebase


router = APIRouter(
    prefix="/mobile/driver/order",
    tags=['Orders driver']
)


   

@router.post("/status", status_code=status.HTTP_200_OK)
def update_order_status_by_driver(order_status: schemas.OrderStatus,background_tasks: BackgroundTasks, db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):

        order_query = db.query(models.Order).filter(models.Order.order_id == order_status.order_id)
        driver_query = db.query(models.Driver).filter(models.Driver.user_id == current_user.id)

        order = order_query.first()
        new_status =  order_status.status

        if new_status != "open" and new_status != "assigned" and new_status != "arrived" and new_status != "in_progress" and new_status != "completed" and new_status != "cancel_by_driver":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"order status does not exist")

        if order == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"order with id: {id} does not exist")



        # Handle when driver to try assign to order
        if new_status == "assigned":
            if order.status != "search_car": 
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="order not available")

 
        # # Handle other status
        # if new_status == "arrived" or new_status == "in_progress" or new_status == "completed":
        #     if order.driver_id != current_user.id:
        #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                                 detail="you don't have access to this order")



        driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).order_by(models.Driver.order_id.desc()).first()
        if driver == None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="driver account didn't find")


        # Update order status in db
        order_query.update({"status":new_status,"driver_id":current_user.id}, synchronize_session=False) 
        if new_status == "assigned":
            driver_query.update({"order_id":order_status.order_id, "price":order.price}, synchronize_session=False)  
              
        db.commit()

        # Update order status in firebase
        update_order_status_in_firebase(order_status.order_id,new_status)



        return {
            
                "status":new_status,

        }
       
        # # Update Postgres order table
        # order.driver_id =  current_user.id
        # order_query.update({"driver_id":current_user.id,"status":new_status}, synchronize_session=False)    
        # db.commit()

        # # Update Firestore order table
        # result_code = change_order_status(order.order_id,order.driver_id,new_status)

        # if result_code == 200:
        #     db.commit() 
        #     return order_query.first()


        # else:
        #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     detail="INTERNAL_SERVER_ERROR") 





@router.get('/driver_active_order', status_code=status.HTTP_200_OK)
def get_user_driver_last_order_status(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):

    user = current_user
    if user == None:
        return { 
                   "order": None,
                   "routes":None,
                   "driver":None,
                   }      

    user_id = current_user.id
    
    driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    if driver == None:
        return { 
                   "order": None,
                   "routes":None,
                   "driver":None,
                   }      

    driver_order_id = driver.order_id                        
    if driver_order_id == None or driver_order_id == 0 :
        return { 
                   "order": None,
                   "routes":None,
                   "driver":driver,
                   }      

    # get last order by ORDER DESC
    order = db.query(models.Order).filter(models.Order.order_id == driver_order_id).order_by(models.Order.order_id.desc()).first() 
    order_status = order.status
    if  order_status == "assigned" or order_status == "arrived":  
        routes = db.query(models.Route).filter(models.Route.order_id == driver_order_id).all()
                      
        return {
                    
                    "order":order,
                    "routes":routes,
                    "driver":driver
            }
    else:
        return { 
                   "order": None,
                   "routes":None,
                   "driver":driver,
                   }      






@router.get("/history", )
def get_orders_history(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_id = current_user.id



       # get last order of user if order status == 'assigned','arrived','search_car'
    query = "SELECT * FROM orders WHERE driver_id = '"+str(user_id)+"' ORDER BY order_id DESC"
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
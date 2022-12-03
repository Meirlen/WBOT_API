from app.database import get_db_singleton
from yandex.abc import DriverInfo
from app.models import Order,Driver
from app.fb_helper import update_order_status_in_firebase,update_driver_location_in_firebase,send_push_notification

# Update order status in firebase and local db
# Add driver info in drivers table
def update_order_status_in_db_and_fb(order_id,driver_info:DriverInfo,status):
    print('update_order_status_in_db_and_fb')
    db = get_db_singleton()   

    # Update order status in db
    order_query = db.query(Order).filter(Order.order_id == order_id)
    order_query.update({"status":status}, synchronize_session=False)    
    db.commit()

    # Update order status in firebase
    update_order_status_in_firebase(order_id,status)

    
    if status == "assigned":
        # Add driver info in local db
        new_driver = Driver(
                            driver_name = driver_info.full_name,
                            car_info = driver_info.car_info,
                            price = driver_info.final_cost,
                            order_id = order_id,
                            phone = driver_info.phone_num
                            )

        db.add(new_driver)
        db.commit()
        db.refresh(new_driver)
        

       
        
                        



# DRIVER NOT FOUND, EXPIRED    
def driver_not_found_info_in_db_and_fb(order_id):
    db = get_db_singleton()   

    # Update order status
    order_query = db.query(Order).filter(Order.order_id == order_id)
    order_query.update({"status":"expired"}, synchronize_session=False)    
    db.commit()

    update_order_status_in_firebase(order_id,"expired")



# DRIVER POSITION IN REALTIME   
def update_order_driver_lat_lng(order_id,lat,lng):
    update_driver_location_in_firebase(order_id,lat,lng)
   
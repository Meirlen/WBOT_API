from app.database import get_db_singleton
from app import models, schemas as schemas
from sqlalchemy import and_, or_
from datetime import datetime, timezone
from app.wati_msg_builder import *
from yandex.order_crud_status import driver_not_found_info_in_db_and_fb


def update_order_status(order_id,new_status,db):
    order_query = db.query(models.Order).filter(models.Order.order_id == order_id)
    order_query.update({"status":new_status}, synchronize_session=False)    
    db.commit()


def get_active_orders():
    yandex_order_ids = []
    ids = []
    db = get_db_singleton()


    # get last order of user if order status == 'assigned','arrived','search_car'
    query = "SELECT * FROM orders WHERE order_id IN (SELECT MAX(order_id) FROM orders  GROUP BY user_id) and status IN ('assigned','arrived','search_car');"
    rs = db.execute(query)

    
    curr_time = datetime.now(timezone.utc)
    print("Current time: ", curr_time)
    counter = 0

    for row in rs:
        counter +=1

        order_id = row['order_id']
        order_time = row['created_at']
        status = row['status']
        user_id = row['user_id']


        difference =  curr_time - order_time
        duration_in_s = difference.total_seconds()
        minutes = divmod(duration_in_s, 60)[0] 
        print("Order created ", minutes , " min ago")
        print(row['order_id']," ",row['status'],"                  User: ",row['user_id'])


        if status == "assigned" or status == "arrived":
            if minutes > 15: 
                # db = next(get_db())
                user = db.query(models.User).filter(models.User.id == user_id).first()
                update_order_status(order_id,"completed",db)
                phone_number = user.phone_number
                # //send_order_completed_message(phone_number,user_id) 
                print("Спасибо за поездку!")

        if status == "search_car":
            # Нужно доработать логику когда будем подключать другие такси
            # Как в яндекс реализаций будем запрашивать текущий статус заказа у агрегаторов
            if minutes > 6: 
                # db = next(get_db())
                user = db.query(models.User).filter(models.User.id == user_id).first()
                update_order_status(order_id,"expired",db)
                driver_not_found_info_in_db_and_fb(order_id)
                phone_number = user.phone_number

                # send_driver_not_found(phone_number,user_id) 
                print("К сожалению нет свободных машин!")  
       
        print('---------------------------------------')
    db.close()
    if counter<1:
       print("Нет активных заказов")



def run_get_status_def():
    while True :
        start_time = time.time()
        get_active_orders()
        print("--- %s seconds ---" % (time.time() - start_time))    
        time.sleep(30)




run_get_status_def()        
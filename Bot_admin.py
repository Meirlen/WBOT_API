from yandex.abc import *
from admin.telegram_api import *
from app.database import get_db_singleton
from yandex.order_crud_status import update_order_status_in_db_and_fb

def send_driver_info_message(order_id,status,phone_num):
    driver_name = "Miras"
    car_color = "красный"
    car_model = "МЕРСЕДЕС"
    plates ="145"
    price ="500"
    rating = "5"

    car_info = str(car_color) +' ' +str(car_model) +' ' + str(plates)
    driver_info = DriverInfo(full_name = driver_name,car_info=car_info,phone_num=phone_num,final_cost=price)

    if status == "assigned":
       driver_info.title = "💁 *- К вам выехала машина.*\n\n*"

    if status == "arrived":
       driver_info.title = "💁 *- Вас ожидает такси.*\n\n*"  


    update_order_status_in_db_and_fb(order_id,driver_info,status)



# send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ Поступил НОВЫЙ ЗАКАЗ! \n The token has expired.')
# send_driver_info_message(2,"arrived","77711474766")    
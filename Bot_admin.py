from yandex.abc import *
from admin.telegram_api import *


def send_driver_info_message(status,phone_num):
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



    db = next(get_db())
    user = db.query(models.User).filter(models.User.phone_number == phone_num).first()   

    send_driver_assigned_info_to_whatsapp(user.id,driver_info,status)



# send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ Поступил НОВЫЙ ЗАКАЗ! \n The token has expired.')
send_driver_info_message("arrived","77711474766")    
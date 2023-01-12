from email import message_from_binary_file
from app.wati import *
import time



def send_greet_message(phone_number,name):
    msg = '💁 Привет <b>'+str(name)+'!</b> ✋\n\n'
    msg += 'Вас приветствует Сапар Бот!\n🚕 . Я помогу Вам зарегистрироваться в приложении Sapar в качестве водителя.\n\n Давайте начнем с основной информации. Напишите мне ФИО полностью. '
    # time.sleep(5) 
    send_message(phone_number,msg)
    # send_template_ask_fill_address(phone_number,user_id)




def send_ask_driver_pasport(phone_number):
    msg = '💁 Сфотогрофируйте и скиньте мне фото <b>Водительского удостворение (Лицевая сторона)</b>:'
    send_message(phone_number,msg)


def send_ask_driver_pasport2(phone_number):
    msg = '💁 Отлично, теперь сфотогрофируйте и скиньте мне фото <b>Водительского удостворение (Обратная сторона)<b>:\n\n'
    send_message(phone_number,msg)



def send_ask_driver_pasport3(phone_number):
    msg = '💁Нужно подтвердить личность\n\n Cделайте фото вместе с водительским удостворением \n\n'
    msg += 'Фото должно быть сделано при хорошем качестве'
    # time.sleep(5) 
    send_message(phone_number,msg)
    # send_template_ask_fill_address(phone_number,user_id)






def send_ask_car_info(phone_number):
    msg = '💁 Давайте теперь заполним информацию о вашем <b>авто<b>\n\n'
    msg += 'Напишите <b>марка/модель авто<b>, Например: Toyota Camry'
    # time.sleep(5) 
    send_message(phone_number,msg)


def send_ask_car_info2(phone_number):
    msg = '💁 <b>Гос номер:<b>\n\n'
    # time.sleep(5) 
    send_message(phone_number,msg)



def send_ask_car_info2_1(phone_number):
    msg = '💁  <b>Цвет авто:<b>\n\n'
    # time.sleep(5) 
    send_message(phone_number,msg)


def send_ask_car_info2_2(phone_number):
    msg = '💁 <b>Год выпуска:<b>\n\n'
    # time.sleep(5) 
    send_message(phone_number,msg)

def send_ask_car_info2_3(phone_number):
    msg = '💁 <b>Кузов:</b>\n'
    msg += '(седан,универсал,кроссовер,хэтчбек,минивэн,лифтбэк,джип итд)'

    # time.sleep(5) 
    send_message(phone_number,msg)


def send_ask_car_info3(phone_number):
    msg = '💁 Отлично, теперь отправьте мне фото:  \n\n'
    msg += 'Тех паспорт (Лицевая сторона)'
    # time.sleep(5) 
    send_message(phone_number,msg)
    # send_template_ask_fill_address(phone_number,user_id)


def send_ask_car_info4(phone_number):
    msg = '💁 Отлично, теперь отправьте мне фото:  \n\n'
    msg += 'Тех паспорт (Обратная сторона)'
    # time.sleep(5) 
    send_message(phone_number,msg)



def send_ask_car_info5(phone_number):
    msg = '💁 Сфотогрофируйте ваш транспорт и скиньте мне \n\n'
    msg += 'На фото должен быть виден госномер'
    send_message(phone_number,msg)




def send_ask_profile_1(phone_number):
    msg = '💁 Шаг - последний, давайте сделаем фото для профиля в приложении Sapar. Отправьте мне свое фото \n\n'
    # time.sleep(5) 
    send_message(phone_number,msg)



def send_reg_completed(phone_number):
    msg = '💁 <b> Заявка принята!</b> ✋\n\n'
    msg += 'Проверка займет до 4 часов, после того как мы проверим вашу заявку в вас будет доступ к заказам в приложении Sapar. \n\n'
    msg += 'По дополнительным вопросам можете написать в тех поддержку: +77711474766 \n\n'

    # time.sleep(5)     # time.sleep(5) 
    send_message(phone_number,msg)









def send_template_ask_fill_address(phone_number,user_id):
    rows = []
    rows.append(TemplateRow("1","?user_id="+str(user_id)))
    request_body = TemplateRequestBody('find_car','find_car',rows)
    send_template(phone_number,request_body)


def search_car_state(body_content):
    
    print('create_body_order_confirm_ask_after_template')

    body_content = pre_proccess_text(body_content)
    footer = None
    header =''
    rows = []
    rows.append(Button("⭕ Отмена"))

    footer = None

    request_body = ButtonsRequestBody(header, body_content,footer,rows)
    return request_body

def order_body(from_address,to_address,aggregator,tariff,price,comment):
    
        price_trip = "Какой то текст"


        msg = "🕒 <b>Идет поиск машины....<b>"+'\n\n'+ "_Ожидайте сообщения с номером автомобиля_\n\n"

        msg += '▪️ <b>' + str(from_address).strip()+'</b>\n'
        if to_address != 'STR' and to_address != None:
            msg += '▪️ <b>' + str(to_address.strip())+'</b>\n\n'

        if comment != None:
           msg += '\n 💬 <b>Комментарий:</b>' + comment+''     
        msg += '\n 🚖 Такси <b>' + aggregator+',</b> ' + tariff+''
        msg += '\n 🪙 <b>' + str(price)+' ₸</b>'

        
    
        # # msg +=  '\n\n🚕  <b>' + price_trip+'</b>'

        # if comment != None and str(comment) != 'not':
        #     msg += '\n\n<i>«' + comment+'» </i>\n'

        return msg


def send_order_info(phone_number,from_address,to_address,aggregator,tariff,price,comment):
    
    send_message_with_buttons(phone_number,search_car_state(order_body(from_address,to_address,aggregator,tariff,price,comment)))
        
def send_price_info(phone_number, yandex_econom, yandex_bussines):
    send_message_with_buttons(phone_number,price_list_with_btn("'💁 *- Тарифы в Яндекс Такси*", yandex_econom, yandex_bussines))


def send_car_search_info(phone_number):
    rows = []
    footer = None
    header =''
    body = '💁 *- Мы приняли ваш заказ.*\n\n _Идет поиск машины..._\n_Ожидайте сообщения с номером автомобиля_'
    # rows.append(Button(CREATE_NEW_ORDER))
    rows.append(Button("⭕ Отмена"))
    request_body = ButtonsRequestBody(header, body,footer,rows)
    send_message_with_buttons(phone_number,request_body)


def sended_car_info(phone_number,msg):
    rows = []
    footer = None
    header =''
    body = msg
    # rows.append(Button(CREATE_NEW_ORDER))
    rows.append(Button("⭕ Отмена"))
    request_body = ButtonsRequestBody(header, body,footer,rows)
    send_message_with_buttons(phone_number,request_body)


from yandex.abc import DriverInfo

def send_driver_assigned_info(phone_number,driver_info:DriverInfo):
    rows = []
    footer = None
    header =''
    body = str(driver_info.title) + str(driver_info.car_info) + "*\nВодитель:\n" + str(driver_info.full_name) + "\n" + str(driver_info.phone_num)+ "\n Стоимость поездки: *" + str(driver_info.final_cost)+"*"
    # rows.append(Button(CREATE_NEW_ORDER))
    rows.append(Button("⭕ Отмена"))
    request_body = ButtonsRequestBody(header, body,footer,rows)
    send_message_with_buttons(phone_number,request_body)





def send_driver_not_found(phone_number,user_id):

    body = '💁 *-К сожалению машина не найдена. Вы сможете продолжить поиск в других агрегаторах.*'

    send_message(phone_number,body)
    send_template_ask_fill_address(phone_number,user_id)


def send_order_completed_message(phone_number,user_id):

    body = '💁 *-Спасибо за поездку!*\n *Не забудьте сохранить нашего бота у себя в контактах.*'

    send_message(phone_number,body)
    send_template_ask_fill_address(phone_number,user_id)

# def send_car_find_info(phone_number):
#     rows = []
#     footer = None
#     header =''
#     body = '💁 *- Мы нашли вам машину.*\n\n _к вам выехала мазда 666 с гос номером 897_\n_Ожидайте.._'
#     # rows.append(Button(CREATE_NEW_ORDER))
#     rows.append(Button("🚕 Карта"))
#     rows.append(Button("⭕ Отмена"))
#     request_body = ButtonsRequestBody(header, body,footer,rows)
#     send_message_with_buttons(phone_number,request_body)






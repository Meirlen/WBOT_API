from app.wati import *
import time



def send_greet_message(phone_number,name,user_id):
    msg = '💁 Привет <b>'+str(name)+'!</b> ✋\n\n'
    msg += 'Вас приветствует сервис Сравни Такси!\n🚕 .'
    # time.sleep(5) 
    send_message(phone_number,msg)
    send_template_ask_fill_address(phone_number,user_id)


def send_template_ask_fill_address(phone_number,user_id):
    rows = []
    rows.append(TemplateRow("1",user_id))
    request_body = TemplateRequestBody('ask_fill_address','ask_fill_address',rows)
    send_template(phone_number,request_body)




def order_body(from_address,to_address):
    
        price_trip = "Какой то текст"
        comment = "Какой то текст"


        msg = "Ваш заказ сформирован, теперь мы сформируем оплату на всех такси агрегаторах на текущиц момент"+'\n\n'
        msg += '🔹 <b>' + str(from_address).strip()+'</b>\n\n'
        if to_address != 'STR' and to_address != None:
            msg += '🔸 <b>' + str(to_address.strip())+'</b>\n'

   
        
    
        msg +=  '\n\n🚕  <b>' + price_trip+'</b>'

        if comment != None and str(comment) != 'not':
            msg += '\n\n<i>«' + comment+'» </i>\n'

        return msg


def send_order_info(phone_number,from_address,to_address):
    send_message(phone_number,order_body(from_address,to_address))
        
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


def send_car_find_info(phone_number):
    rows = []
    footer = None
    header =''
    body = '💁 *- Мы нашли вам машину.*\n\n _к вам выехала мазда 666 с гос номером 897_\n_Ожидайте.._'
    # rows.append(Button(CREATE_NEW_ORDER))
    rows.append(Button("🚕 Карта"))
    rows.append(Button("⭕ Отмена"))
    request_body = ButtonsRequestBody(header, body,footer,rows)
    send_message_with_buttons(phone_number,request_body)




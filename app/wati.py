
import requests
from dataclasses import dataclass
import json
from typing import List
import dataclasses
from app.app_constans import *
import shutil


# Whatsapp Settings
WHATSAPP_WEBHOOK_URL = "https://live-server-9232.wati.io"
WHATSAPP_API_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI2MGI0YTFlMi1hMDY0LTRhNDUtYThhYy03NjYwNWQyNGNlMmMiLCJ1bmlxdWVfbmFtZSI6Im1pa29fOTgyQG1haWwucnUiLCJuYW1laWQiOiJtaWtvXzk4MkBtYWlsLnJ1IiwiZW1haWwiOiJtaWtvXzk4MkBtYWlsLnJ1IiwiYXV0aF90aW1lIjoiMTAvMjAvMjAyMiAwODoyODoxMSIsImRiX25hbWUiOiI5MjMyIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQURNSU5JU1RSQVRPUiIsImV4cCI6MjUzNDAyMzAwODAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.UfIJnAV6ZEDNTL1ewrnZpJOa2fCRzOhiNuG0VRyyKxs'

def update_whatsapp_token(new_token):
   print('Token wati updated')
   global WHATSAPP_API_TOKEN
   WHATSAPP_API_TOKEN = new_token
   print(WHATSAPP_API_TOKEN)



@dataclass
class MenuRow:
    title: str
    description: str = None


@dataclass
class MenuSection:
    title: str
    rows:List[MenuRow]

@dataclass
class Button:
    text:str


@dataclass
class MenuRequestBody:
    header:str = None
    body: str  = None
    footer:str = None
    buttonText: str  = None
    sections:List[MenuSection] = None


@dataclass
class ButtonsRequestBody:
    header:str = None
    body: str  = None
    footer:str = None
    buttons:List[Button] = None


@dataclass
class TemplateRow:
    name: str
    value: str = None

@dataclass
class TemplateRequestBody:
    template_name:str
    broadcast_name: str  
    parameters:List[TemplateRow]




def create_body_cancel_order(body_content):
    rows = []
    rows.append(MenuRow("⭕ Отмена"))


    sections = [MenuSection("Выберите действие",rows)]

    request_body = MenuRequestBody(body_content, "Меню",sections)
    return request_body


def create_body_login(name,phone_number):
    rows = []
    rows.append(TemplateRow("name","*"+name+"*"))
    rows.append(TemplateRow("phone_number","*"+phone_number+"*"))

    request_body = TemplateRequestBody('phone_confirm','phone_confirm',rows)

    return request_body    


def create_body_ask_apart(from_address):
    rows = []
    rows.append(TemplateRow("from","*"+from_address+"*"))

    request_body = TemplateRequestBody('skip_fill_form','skip_fill_form',rows)

    return request_body   

def create_body_order_confirm():
    rows = []
    rows.append(TemplateRow("title"," - Чтобы заказать такси сейчас,  нажмите на кнопку "))
    rows.append(TemplateRow("body"," *Заказать.* "))

    request_body = TemplateRequestBody('confirm_order','confirm_order',rows)

    return request_body   


def create_body_ask_to_address(from_address):

    rows = []
    rows.append(MenuRow("⭕ Отмена"))

    sections = [MenuSection("Выберите действие",rows)]

    header = ""
    body = '💁 *- ok, c  '+from_address.strip()+'*  Куда поедем?'
    body = '- адрес подачи авто: _'+from_address.strip()+'_\n\n💁  - *Куда поедем*?'
    # footer = '🔸 Куда: _не заполнено_ \n\n'
    # if len(footer) > 59:  # max lenght 60
    #    body = body + '\n\n' + footer
    #    footer = None 
    footer = ''

    # request_body = MenuRequestBody(header, body,footer,"Меню",sections)

    return body   


def create_body_finish_state(body):

    rows = []
    rows.append(MenuRow(CREATE_NEW_ORDER))
    rows.append(MenuRow("⭕ Отмена"))

    sections = [MenuSection("Выберите действие",rows)]

    header = ""
    footer = ''

    request_body = MenuRequestBody(header, body,footer,"Меню",sections)

    return request_body     


def create_body_templates(body,templates):

    rows = []
    for template in templates:
        rows.append(MenuRow(template.title,template.description))

    sections = [MenuSection("Выберите из списка:",rows)]

    header = ""
    footer = ''

    request_body = MenuRequestBody(header, body,footer,"Шаблоны",sections)

    return request_body     


def create_body_after_order_created_state(body_content,full = True):

    body_content = pre_proccess_text(body_content)


    rows = []
    if full:
        rows.append(MenuRow(CONFIRM_ORDER_BTN_TITLE,"Мы отправим вам такси по данному адресу"))
        rows.append(MenuRow(ADD_COMMENT_BTN_TITLE))
        rows.append(MenuRow("⭕ Отмена"))
    else:
        rows.append(MenuRow(CREATE_NEW_ORDER))
        rows.append(MenuRow("⭕ Отмена"))

        

    sections = [MenuSection("Выберите действие",rows)]
    header =''
    body = str(body_content.split('[header]')[0])+'\n\n'
    # body = TITLE_AFTER_CREATED_ORDER+'\n\n'
    body +=  body_content.split('[header]')[1].split('[body]')[0]
    footer =  body_content.split('[footer]')[1]
    # price = body_content.split('[footer]')[1]

    # footer = BOT_CALC_COST_WARNING_MESSAGE   
    if len(footer) > 59:  # max lenght 60
       body = body + '\n' + footer
       footer = None 

    request_body = MenuRequestBody(header, body,footer,"Меню",sections)


    return request_body


def create_body_order_confirm_ask(body_content,full = True):

    body_content = pre_proccess_text(body_content)
    footer = None
    header =''

    rows = []
    if full:

        body = str(body_content.split('[header]')[0])+'\n\n'
        # body = TITLE_AFTER_CREATED_ORDER+'\n\n'
        body +=  body_content.split('[header]')[1].split('[body]')[0]
        footer_body =  body_content.split('[footer]')[1]
    
        body = body+'\n'+ footer_body

        print(body_content.split('[header]')[0])
        print(body_content.split('[footer]')[1])
        rows.append(Button(CONFIRM_ORDER_BTN_TITLE))
        # rows.append(MenuRow(ADD_COMMENT_BTN_TITLE))
        rows.append(Button("⭕ Отмена"))
        footer = "Чтобы вызвать такси нажмите на кнопку *Заказать*"
    else:

        body = '💁 *- Мы приняли ваш заказ.*\n\n _Идет поиск машины..._\n_Ожидайте сообщения с номером автомобиля_'
        # rows.append(Button(CREATE_NEW_ORDER))
        rows.append(Button("⭕ Отмена"))

    request_body = ButtonsRequestBody(header, body,footer,rows)


    return request_body




def price_list_with_btn(body_content, yandex_econom, yandex_bussines):
    
    print('create_body_order_confirm_ask_after_template')

    body_content = pre_proccess_text(body_content)
    footer = None
    header =''
    rows = []
    rows.append(Button("🚕 "+ yandex_econom))
    rows.append(Button("🚕 "+ yandex_bussines))

    # # rows.append(Button(CONFIRM_9_REGION_BTN_TITLE))
    # rows.append(Button(CONFIRM_ALEM_BTN_TITLE))

    footer = "Чтобы вызвать такси нажмите на кнопку *Заказать*"

    request_body = ButtonsRequestBody(header, body_content,footer,rows)
    return request_body


def create_body_order_templates(templates,title):
    
    header =''
    body = '🚕 *МАШИНА ПОДЬЕХАЛА!* \n\n'+title+'\n\nЧтобы создать *новый заказ* вы можете просто написать адресс. \nЛибо выбрать из списка *шаблонов* внизу:'
    footer = 'Шаблоны - ваши последние поездки'

    rows = []

    for template in templates:
        rows.append(Button(template))



    request_body = ButtonsRequestBody(header, body,footer,rows)


    return request_body


def create_body_multiple_address_case(title,address_list,desc_list):
    
    rows = []
    for i in range(len(address_list)):
        rows.append(MenuRow(address_list[i][:24],desc_list[i])) # max lenght of title in the wati api

    sections = [MenuSection("Выберите из списка",rows)]
    request_body = MenuRequestBody(None, title,None,"Выбрать из списка",sections)


    return request_body


    

# print(json_request_body)


def handle_token_expired(response):
    if response.status_code == 401:
        print('UNAUTHORIZED')   
        # send_message_to_telegram_chat(ADMIN_CHAT_ID,'⚡ ⛔ Whatsapp api  Error!!! \n The token has expired.')


def send_message(whatsapp_number,message):
    print('send_message')
    message = pre_proccess_text(message)
    token = WHATSAPP_API_TOKEN
    url = WHATSAPP_WEBHOOK_URL

    method  = 'sendSessionMessage'
    url+='/api/v1/{0}/{1}'.format(method,whatsapp_number)
    print(token)

    response = requests.post(
            url = url,
            headers={"Authorization":"Bearer "+token},
            data={'messageText': message}
        )

    handle_token_expired(response)

    print(response) 



def send_message_with_menu(whatsapp_number,body:MenuRequestBody):

    # convert data class to json
    body = json.dumps(dataclasses.asdict(body)) # '{"x": "1"}'
    print("send_message_with_menu Body:")


    token = WHATSAPP_API_TOKEN
    url = WHATSAPP_WEBHOOK_URL

    method  = 'sendInteractiveListMessage'
    url+='/api/v1/{0}?whatsappNumber={1}'.format(method,whatsapp_number)

    response = requests.post(
            url = url,
            headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"},
            data=body 
        ).json()

    print(response)


def send_message_with_buttons(whatsapp_number,body:ButtonsRequestBody):

    # convert data class to json
    body = json.dumps(dataclasses.asdict(body)) # '{"x": "1"}'
    print("send_message_with_buttons Body:")


    token = WHATSAPP_API_TOKEN
    url = WHATSAPP_WEBHOOK_URL

    method  = 'sendInteractiveButtonsMessage'
    url+='/api/v1/{0}?whatsappNumber={1}'.format(method,whatsapp_number)

    response = requests.post(
            url = url,
            headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"},
            data=body 
        ).json()

    print(response)


def send_template(whatsapp_number,body:TemplateRequestBody):

    # convert data class to json
    body = json.dumps(dataclasses.asdict(body)) # '{"x": "1"}'
    
    whatsapp_number = "8"+whatsapp_number[1:] # wati phone format difference between to send_message and send_template

    token = WHATSAPP_API_TOKEN
    url = WHATSAPP_WEBHOOK_URL
    

    method  = 'sendTemplateMessage'
    url+='/api/v1/{0}?whatsappNumber={1}'.format(method,whatsapp_number)

    response = requests.post(
            url = url,
            headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"},
            data=body 
        ).json()

    # print(response)

import re
def pre_proccess_text(text):


    text = text.replace('  </b>','</b>').replace(' </b>','</b>').replace('</b>','*').replace('<b>','*')
    text = text.replace('</i>','```').replace('<i>','```')

    # text = text.replace(' *','*').replace('* ','*')
    return text




def get_media(data):
    print('get_media')
    file_name = data.split('fileName=')[1]
    token = WHATSAPP_API_TOKEN
    url = WHATSAPP_WEBHOOK_URL


    method  = 'getMedia'
    url+='/api/v1/{0}'.format(method)
    local_filename = 'user_audio.ogg'

    with requests.get(
            url = url,
            headers={"Authorization":"Bearer "+token},
            data={'fileName': file_name},
            stream=True
        ) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


    # text = transcribe_audio().lower()
    text = "zxcxc"
    return text


            
# send_message_with_menu("77774857133",create_body_finish_state("💁 - Чтобы заказать такси напишите *Откуда* и *Куда* поедете?\n\n Примеры: \n_«c 12 13 16 поедем на Восток 2»_\n_«с Алиханова 7 квартира 89 на цум»_\n\n"))

# send_message("77752632438",'Bot says')
# templates = []
# templates.append('ануара 15- микр ')

# title = "Такси 'ADAM 503-503' Вас ожидает Серебристый Мерседес 154"

# send_message_with_buttons("77774857133",create_body_order_templates(templates,title))

# webhook_url = "https://live-server-9232.wati.io"
# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3ODhkMGU2Ni05OTJjLTRjOGQtYTg1Ni05ZmZkOTRjMzFiMzAiLCJ1bmlxdWVfbmFtZSI6Im1pa29fOTgyQG1haWwucnUiLCJuYW1laWQiOiJtaWtvXzk4MkBtYWlsLnJ1IiwiZW1haWwiOiJtaWtvXzk4MkBtYWlsLnJ1IiwiYXV0aF90aW1lIjoiMDUvMjAvMjAyMiAwODo1NzozNyIsImRiX25hbWUiOiI5MjMyIiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiQURNSU5JU1RSQVRPUiIsImV4cCI6MjUzNDAyMzAwODAwLCJpc3MiOiJDbGFyZV9BSSIsImF1ZCI6IkNsYXJlX0FJIn0.ybykJSB7MvWxmhDbb4QvsEWGTBFmjl2o1EnXqQhq_Ak'
# data = create_body_order_confirm_ask("[header]Готово[body]цум, проспект бухар жырау,[footer] 🚕 с города на юг 500 ",True)
# send_message_with_buttons('77774857133',data)
# # body_content = '🔹 <b>цум, проспект бухар жырау, 53/8</b>\n\n🔸 <b>язева</b>\n\n\n🚕 с города на юг 500  ₸'
# channel = Wati(token,webhook_url)
# print(channel.get_media("https://live-server-9232.wati.io/api/file/showFile?fileName=data/audios/4a935748-1c38-4c26-af36-3ce67ae261d8.opus"))





def get_messages(whatsapp_number):
    print('get_messages')
    token = WHATSAPP_API_TOKEN
    url = WHATSAPP_WEBHOOK_URL

    method  = 'getMessages'
    url+='/api/v1/{0}/{1}'.format(method,whatsapp_number)

    response = requests.get(
            url = url,
            headers={"Authorization":"Bearer "+token},
            data={  
                'pageSize': 1000,
                    'pageNumber': 1,
            }
        ).json()
    response_array = response['messages']['items']
    return response_array
   


def get_contacts():
    print('get_contacts')
    token = WHATSAPP_API_TOKEN
    url = WHATSAPP_WEBHOOK_URL

    method  = 'getContacts'
    url+='/api/v1/{0}'.format(method)

    response = requests.get(
            url = url,
            headers={"Authorization":"Bearer "+token},
            data={  
                'pageSize': 1000,
                'pageNumber': 1,
            }
        ).json()
    response_array = response['contact_list']
    print('All conversations: ',len(response_array))
    return response_array
   


# create_body_ask_to_address("mjnnn")
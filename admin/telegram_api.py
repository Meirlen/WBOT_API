
from app.app_constans import *
import requests


    

def send_message_to_telegram_chat(chat_id,text):
    # print(text)
    token = TELEGRAM_HTTP_ACCESS_TOKEN
    method  = 'sendMessage'

    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            data={'chat_id': chat_id, 'text': text,'parse_mode': 'html'}
        ).json()

    # print(response)  


def send_message_to_telegram_chat_with_buttons(query):

    token = TELEGRAM_HTTP_ACCESS_TOKEN
    method  = 'sendMessage'

    response = requests.get(
            url='https://api.telegram.org/bot{0}/sendMessage?{1}'.format(token, query),
        ).json()

    print(response)  


def send_file_to_telegram_chat(chat_id):
    token = TELEGRAM_HTTP_ACCESS_TOKEN
    method  = 'sendDocument'
    files = {'document': open('krg_address.db', 'rb')}
    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            files=files,
            data={'chat_id': chat_id}
        ).json()

    print(response)      






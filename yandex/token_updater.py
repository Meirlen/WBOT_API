import requests
from yandex.json_data import *
from yandex.yandex_config import * 
import json


def update_yandex_token(new_token):

    

    json_data = {
                "token": new_token
                }
    response = requests.post('https://02qyk.localtonet.com/webhook/yandex_token_update',json=json_data)

    print(response.status_code)


def get_new_token():

    json_data = {}

    response = requests.post('https://ya-authproxy.taxi.yandex.kz/csrf_token', cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)

    print(text)
    print(response.status_code)

    if response.status_code == 401:
        print("Unauthorized 401")
    if response.status_code == 200: 
        print("Yahoooooooooooo")
        return text['sk'] 
 

    return None



import time
def update_token_by_timer():
    while True :
        print("Yandex token successfully updated")
        new_token = get_new_token()
        update_yandex_token(new_token)
        time.sleep(1800)

# update_token_by_timer()
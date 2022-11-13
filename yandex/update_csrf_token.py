import json
import requests
from yandex.json_data import *
from yandex.yandex_config import * 




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
    
   
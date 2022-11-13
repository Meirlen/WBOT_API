suggest_url = "https://ya-authproxy.taxi.yandex.ru/integration/turboapp/v1/suggest"



import json
import requests
from json_data import *
from yandex_config import *





def search_address_with_suggest():
    
    json_data = {
                "part": "назарбаева",
                "type": "a",
                "id": x_yataxi_userid,
                "state": {
                    "accuracy": 0,
                    "location": [
                    73.1332356264,
                    49.7743451715
                    ]
                },
                "position": [
                    73.1332356264,
                    49.7743451715
                ],
                "action": "user_input",
                "sticky": False
            }

    response = requests.post("https://ya-authproxy.taxi.yandex.ru/integration/turboapp/v1/suggest", cookies=cookies, headers=headers,
                             json=json_data)

    text = json.loads(response.text)



    print(text)
    print(response.status_code)

    if response.status_code == 401:
        print("Unauthorized 401")
    if response.status_code == 200:  
        print(text)  




search_address_with_suggest()
import json
import requests
from yandex.json_data import *
from yandex.yandex_config import * 

from yandex.data_models import *

from app.database import get_db
from app import models, schemas as schemas
from app.wati_msg_builder import *


def get_saved_last_token():
     db = get_db()
     csrf_token = next(db).query(models.Credentials).filter(models.Credentials.name == "csrf_token").first()
     return csrf_token.value      

def get_price_by_route(routes):

    result = None

    json_data = calc_price_json_data
    json_data['id'] = x_yataxi_userid
    json_data["route"] = routes

    # set csrf token
    x_csrf_token = os.getenv("CSRF_TOKEN",None)

    if x_csrf_token == None:
        x_csrf_token = get_saved_last_token()
        os.environ["CSRF_TOKEN"] = x_csrf_token
        print("Token from db: ", x_csrf_token )

    headers['x-csrf-token'] =  x_csrf_token



    print("Yandex csrf Token: ", x_csrf_token)



    try:
        response = requests.post('https://ya-authproxy.taxi.yandex.kz/3.0/routestats', cookies=cookies, headers=headers,
                             json=json_data)

        text = json.loads(response.text)



        # print(text)
        print(response.status_code)

        if response.status_code == 401:
            print("Unauthorized 401")
        if response.status_code == 200:
            result = [] 
            for trip_type in text['service_levels']:
                trip_price = trip_type['price'].replace('$SIGN$$CURRENCY$', 'T')
                result.append({"name_tariff": trip_type['name'],"price":trip_price})
                print(f"{trip_type['name']} - {trip_price}")



        return result

    except :
        print("Error")
        return None



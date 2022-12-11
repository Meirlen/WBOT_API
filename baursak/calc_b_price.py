from cmath import cos
import json
import requests
from baursak.baursak_config import *
from baursak.json_data import *
import uuid





def get_price_by_route_baursak(routes):

    result = None

    json_data = calc_price_json_data
    headers['X-Request-Id'] = str(uuid.uuid4())

    addresses = []
    for route in routes:
        addresses.append({
                        "lat":route[1],
                        "lon":route[0],
                        "stop_duration": 0

        })
    json_data["addresses"] = addresses


    try:
        response = requests.post('https://relay.platform.taximaster.ru:8089/taxi_caller_api/1.10/calc_order_cost', headers=headers,
                             json=json_data)



        try:
            response_json = json.loads(response.text)

            if response.status_code == 401:
                print("Unauthorized 401")
            if response.status_code == 200:
                result = [] 

                # print(response_json)
                costs = response_json['data']['costs']
                for cost in costs:
                    result.append({
                                  "price":str(cost['cost']),
                                  "tariff_name":cost['crew_group_id']
                                  })
      

            return result
        except:
            print("Error")


    except Exception as e:
        print("Error" , e )

    return None

# routes = [[73.086701,49.80339],[72.870346,49.632961]]
# get_price_by_route_baursak(routes)


from cmath import cos
import json
import requests
from region.region_config  import *
from region.json_data import *
import uuid





def get_price_by_route_region(routes):

    result = None

    json_data = calc_price_json_data

    addresses = []
    for route in routes:
        addresses.append({
                        "lat":route[1],
                        "lon":route[0],

        })
    json_data["route"] = addresses


    try:
        response = requests.post('https://client-app-proxy.pk.kz/api/client/mobile/4.0/estimate', headers=headers,
                             json=json_data)


        print(response)

        try:
            response_json = json.loads(response.text)
            print(response.status_code)

            if response.status_code == 401:
                print("Unauthorized 401")
            if response.status_code == 200:
                result = [] 

                # print(response_json)
                costs = response_json['estimations']
                for cost in costs:
                    result.append({
                                  "price":str(int(cost['cost']['amount'])),
                                  "tariff_name":cost['tariff']
                                  })
      

            return result
        except:
            print("Error")


    except Exception as e:
        print("Error" , e )

    return None

# routes = [[73.086701,49.80339],[72.870346,49.632961]]


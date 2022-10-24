


[
    {
    "short_text": "улица Алиханова, 13",
    "geopoint": [
        73.088504,
        49.807754
    ],
    "fullname": "Караганда, улица Алиханова, 13",
    "type": "address",
    "city": "Караганда",
    },
    {
    "short_text": "Ясли-сад Еркетай",
    "geopoint": [
        73.151855,
        49.782448
    ],
    "fullname": "Казахстан, Караганда, микрорайон Степной-1, 7А, Ясли-сад Еркетай",
    "type": "organization",
    "city": "Караганда",
    }
]



from dataclasses import dataclass
from typing import List


@dataclass
class YandexRoute():
        short_text:str
        geopoint:List[float]
        fullname:str
        type:str
        city:str



route_1 = YandexRoute("улица Алиханова, 13",[73.088504,49.807754],"Караганда, улица Алиханова, 13","address","Караганда")
route_2 = YandexRoute("Ясли-сад Еркетай",[73.151855,49.782448],"Казахстан, Караганда, микрорайон Степной-1, 7А, Ясли-сад Еркетай","organization","Караганда")
routes = [route_1,route_2]
# print(routes)
# body = json.dumps(dataclasses.asdict(body))



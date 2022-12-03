

from yandex.abc import *
from yandex.calc_price import *
from yandex.yandex_geo_coder import *




get_address_by_coords()

# import os

# from app.database import get_db
# from app import models, schemas as schemas
# from app.wati_msg_builder import *





# print(get_saved_last_token())
# os.environ["CSRF_TOKEN"] = "1"

# print(os.getenv("CSRF_TOKEN",None))

#### PRICE CALCULATOR START


# Yandex price calc
from yandex.abc import *
from yandex.calc_price import *


# price_info = get_price_by_route(routes)
# print(price_info)


# # Baursak price calc
# from baursak.calc_b_price import *

# price_info = get_price_by_route_baursak(routes)
# print(price_info)


# Region price calc
# from region.calc_region_price import *


# routes = [[73.132545, 49.77491], [73.076233, 49.915886]]

# price_info = get_price_by_route(routes)
# print(price_info)


#### PRICE CALCULATOR END




# from yandex.update_csrf_token import *

# update_token()

# from yandex.abc import *

# run_get_status_def()
# get_price_by_route(routes)
# update_order_status("712193620d3ad043bf8a94df3f7f13ca")
# send_driver_assigned_info_to_whatsapp(1)

# run_get_status_def()
# # send_driver_not_found_info_to_whatsapp(1)


order = {
  "additional_buttons": {},
  "cost_message": "650 $SIGN$$CURRENCY$",
  "currency_rules": {
    "code": "KZT",
    "cost_precision": 0,
    "sign": "₸",
    "template": "$VALUE$ $SIGN$$CURRENCY$",
    "text": "тенге"
  },
  "dont_call": False,
  "park": {
    "id": "400000841741",
    "legal_address": "050057, Алматы, Жарокова, 129",
    "long_name": "ТОО Pay Systems Kz",
    "name": "My Group",
    "phone": "+77075050880",
    "yamoney": False
  },
  "feedback": {},
  "route_sharing_url": "https://taxi.yandex.ru/route/7aae2c5f3385ca56db0d272ca437f972?lang=ru",
  "dont_sms": False,
  "user_ready": False,
  "final_cost_as_str": "650 $SIGN$$CURRENCY$",
  "final_cost": 650,
  "final_cost_decimal_value": "650",
  "cancel_disabled": False,
  "driverclientchat_enabled": False,
  "drivercall_enabled": True,
  "tariff": {
    "class": "econom",
    "fixed": True,
    "id": "9fece2665f3d48f690616c4a1c5b6ca3",
    "name": "Эконом"
  },
  "payment": {
    "type": "cash"
  },
  "driver": {
    "tag": "9af4120dbc87d3b15cc89a4e366c573707c18be837d0d88cd1b445677899fc17",
    "name": "Егоров Владимир Владимирович",
    "profile_facts": [
      {
        "is_top_value": True,
        "subtitle": "рейтинг",
        "title": "5.0"
      },
      {
        "is_top_value": False,
        "subtitle": "лет стажа",
        "title": "6"
      }
    ],
    "plates": "795АВU09",
    "yellow_car_number": False,
    "rating": "5.0",
    "photo_url": "",
    "overdue": False,
    "phone": "+77780215310,,22319",
    "status_title": "5.0 $RATING$",
    "short_name": "Владимир",
    "model": "Nissan Primera",
    "forwarding": {
      "ext": "22319",
      "phone": "+77780215310"
    },
    "color_code": "0000CC",
    "car_direction": 245,
    "color": "синий",
    "car": [
      73.082433,
      49.812302
    ]
  },
  "version": "DAAAAAAABgAMAAQABgAAAMuveBOEAQAA",
  "tips": {
    "available": False,
    "decimal_value": "0",
    "type": "percent",
    "value": 0
  },
  "status": "waiting",
  "status_updates": [
    {
      "created": "2022-10-26T08:46:13.606+0000",
      "reason": "create",
      "status": "pending"
    },
    {
      "created": "2022-10-26T08:46:20.912+0000",
      "reason": "new_driver_found"
    },
    {
      "created": "2022-10-26T08:46:21.9+0000",
      "reason": "seen_received"
    },
    {
      "created": "2022-10-26T08:46:22.374+0000",
      "reason": "seen"
    },
    {
      "created": "2022-10-26T08:46:26.786+0000",
      "reason": "requestconfirm_assigned",
      "status": "assigned"
    },
    {
      "created": "2022-10-26T08:46:26.786+0000",
      "reason": "requestconfirm_driving"
    }
  ],
  "payment_changes": [],
  "supported_feedback_choices": {
    "low_rating_reason": [
      {
        "label": "Водитель опоздал",
        "name": "driverlate"
      },
      {
        "label": "Грубый водитель",
        "name": "rudedriver"
      },
      {
        "label": "Запах в машине",
        "name": "smellycar"
      },
      {
        "label": "Состояние автомобиля",
        "name": "carcondition"
      },
      {
        "label": "Ездил кругами",
        "name": "badroute"
      },
      {
        "label": "Не было сдачи",
        "name": "nochange"
      }
    ]
  },
  "free_cancel_for_reason": False,
  "pending_changes": [],
  "granted_promotions": [],
  "can_make_more_orders": "not_modified",
  "performer_realtime_info": {
    "position": [
      73.082433,
      49.812302
    ]
  },
  "allowed_changes": [
    {
      "name": "comment"
    },
    {
      "name": "porchnumber"
    },
    {
      "name": "destinations"
    },
    {
      "available_methods": [
        "card"
      ],
      "name": "payment"
    }
  ],
  "typed_experiments": {
    "items": [
      {
        "name": "short_car_plates",
        "value": {
          "enabled": True,
          "short_plate": [
            "car_map_object",
            "state_bar",
            "order_list_item"
          ]
        }
      }
    ],
    "version": 4335937
  },
  "request": {
    "comment": "",
    "cost_centers": {
      "can_change": True,
      "values": []
    },
    "due": "2022-10-26T14:50:22+0600",
    "route": [
      {
        "area": "городской акимат Караганда",
        "areas": [
          "городской акимат Караганда"
        ],
        "city": "Караганда",
        "country": "Казахстан",
        "description": "Караганда",
        "full_text": "Караганда, проспект Бухар Жырау, 53/8",
        "fullname": "Караганда, проспект Бухар Жырау, 53/8",
        "geopoint": [
          73.08615875,
          49.80342102
        ],
        "house": "53/8",
        "locality": "Караганда",
        "object_type": "другое",
        "point": [
          73.08615875,
          49.80342102
        ],
        "premisenumber": "53/8",
        "short_text": "проспект Бухар Жырау, 53/8",
        "short_text_from": "проспект Бухар Жырау, 53/8",
        "short_text_to": "проспект Бухар Жырау, 53/8",
        "street": "проспект Бухар Жырау",
        "thoroughfare": "проспект Бухар Жырау",
        "type": "address",
        "uris": [
          "ymapsbm1://geo?data=Cgg2NzQyNTM3NRJS0prQsNC30LDSm9GB0YLQsNC9LCDSmtCw0YDQsNKT0LDQvdC00YssINCR0rHSm9Cw0YAg0JbRi9GA0LDRgyDQtNCw0qPSk9GL0LvRiywgNTMvOCIKDSQskkIVwDZHQg=="
        ]
      },
      {
        "area": "городской акимат Караганда",
        "areas": [
          "городской акимат Караганда"
        ],
        "city": "Караганда",
        "country": "Казахстан",
        "description": "Караганда",
        "full_text": "Караганда, улица Язева, 1",
        "fullname": "Караганда, улица Язева, 1",
        "geopoint": [
          73.12917328,
          49.77170944
        ],
        "house": "1",
        "locality": "Караганда",
        "object_type": "другое",
        "point": [
          73.12917328,
          49.77170944
        ],
        "premisenumber": "1",
        "short_text": "улица Язева, 1",
        "short_text_from": "улица Язева, 1",
        "short_text_to": "улица Язева, 1",
        "street": "улица Язева",
        "thoroughfare": "улица Язева",
        "type": "address",
        "uris": [
          "ymapsbm1://geo?data=CgoxNDg4MDk3OTA3EkDSmtCw0LfQsNKb0YHRgtCw0L0sINKa0LDRgNCw0pPQsNC90LTRiywg0K/Qt9C10LIg0LrTqdGI0LXRgdGWLCAxIgoNI0KSQhU7FkdC"
        ]
      }
    ],
    "service_level": 0
  },
  "source": [
    73.08615875,
    49.80342102
  ],
  "routeinfo": {
    "time_left": 218,
    "distance_left": 1393
  },
  "classes": [
    "econom"
  ]
}

# handle_driver_object(order,OrderInfo("sdddddddddddc1121",1,"assigned"))

# # run_get_status_def()





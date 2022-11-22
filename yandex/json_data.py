
from .yandex_config import *

calc_price_json_data = {

  "selected_class": "",
  "format_currency": True,
  "requirements": {
    "coupon": ""
  },
  "payment": {
    "type": "cash",
    "payment_method_id": "cash"
  },
  "summary_version": 2,
  "is_lightweight": False,
  "extended_description": True,
  "supported_markup": "tml-0.1",
  "supports_paid_options": True,
  "tariff_requirements": [
    {
      "class": "econom",
      "requirements": {
        "coupon": ""
      }
    },
    {
      "class": "business",
      "requirements": {
        "coupon": ""
      }
    }
  ]
}

create_draft_json_data = {
            "id": x_yataxi_userid,
            "class": [
                "econom"
            ],
            "payment": {
                "type": "cash",
                "payment_method_id": "cash"
            },
            # "offer": "77dc40acc55439359b46af88ae5b122e", Лучше убрать ато по истечению времени выходит ошибка PRICE CHANGED
            "parks": [],
         
            "requirements": {
                "coupon": ""
            },
            "dont_sms": False,
            "driverclientchat_enabled": True
}

geo_coder_json_data = {
  "type": "a",
  "id": "11eb7777c559487e87ebe2728712d034",
  "state": {
    "accuracy": 0,
    "location": [
      73.19400342718102,
      49.87035459240982
    ]
  },
  "position": [
      73.19400342718102,
      49.87035459240982
  ],
  "action": "pin_drop",
  "sticky": False
}
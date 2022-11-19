import requests
from yandex.json_data import *
from yandex.yandex_config import * 
import json
import aiohttp
import asyncio


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


async def get_order(session, new_token):

    url = 'http://165.22.13.172:8000/webhook/yandex_token_update'

    json_data = {
                "token": new_token
                }
    async with session.post(url, json = json_data) as response:
        order = await response.text()
        print("-> Token updated" )

        return order

async def get_orders_status(token):

    async with aiohttp.ClientSession() as session:

        tasks = []

        tasks.append(asyncio.ensure_future(get_order(session,token)))

        await asyncio.gather(*tasks)

import time
def update_token_by_timer():
    while True :
        print("Yandex token successfully updated")
        new_token = get_new_token()
        asyncio.run(get_orders_status(new_token))
        time.sleep(1800)

# update_token_by_timer()
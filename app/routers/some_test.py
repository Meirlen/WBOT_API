import requests
import json

API_YANDEX_URL = 'https://suggest-maps.yandex.ru/suggest-geo?apikey=a4018892-4411-4709-97ea-6881ac674715&v=7&search_type=all&lang=ru_RU&n=50&bbox=72.958828,49.730972~73.267132,49.989920&part=';



# async def suggest(query):

#     async with aiohttp.ClientSession() as session:

#         async with session.get(API_YANDEX_URL+query) as resp:
#             response = await resp.text()
#             response = response.replace("suggest.apply(",'')
#             # response = response[0,-1]
#             print(response)

# asyncio.run(suggest("Наза"))


def suggest(query):


    response = requests.get(API_YANDEX_URL+query)
    response = response.text.replace("suggest.apply(",'')[:-1]

    # text = json.loads(response.text)

    print(response)


suggest("Наза")
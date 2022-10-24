
# Great article about async code
# https://www.mybluelinux.com/asynchronous-http-requests-in-python-with-aiohttp-and-asyncio/

import aiohttp
import asyncio
import time

# start_time = time.time()


# async def main():

#     async with aiohttp.ClientSession() as session:

#         for number in range(1, 151):
#             pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{number}'
#             async with session.get(pokemon_url) as resp:
#                 pokemon = await resp.json()
#                 print(pokemon['name'])

# asyncio.run(main())



# print("--- %s seconds ---" % (time.time() - start_time))




import requests
import time

start_time = time.time()

for number in range(1, 151):
    url = f'https://pokeapi.co/api/v2/pokemon/{number}'
    resp = requests.get(url)
    pokemon = resp.json()
    print(pokemon['name'])

print("--- %s seconds ---" % (time.time() - start_time))
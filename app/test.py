import asyncio

async def update_order_status_in_firebase(i, time):
    print(f"hello {i} started")
    await asyncio.sleep(time)
    print(f"hello {i} done")

async def create_order_test():
    task1 = asyncio.create_task(update_order_status_in_firebase(1,7))  # B
    task2 = asyncio.create_task(update_order_status_in_firebase(2,10))  # C
    print("Something")
    await task1
    await task2

# asyncio.run(create_order())  # main loop

# import time

# async def create_order_in_firebase():


#     # Wait 10 seconds and update order for all drivers = C category
#     await asyncio.sleep(5) 
#     print('Order created and changed')



# async def fast_api_code():
#     task1 = asyncio.create_task(create_order_in_firebase()) 
#     await asyncio.sleep(3)
#     await task1
#     print("All tasks Done")  



# asyncio.run(fast_api_code())



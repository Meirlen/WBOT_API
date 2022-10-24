
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# import time


# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


# db = firestore.client()



# def set_order_in_firebase(order_id,from_address,to_address,price,from_lat,from_lng,to_lat,to_lng,visibilty):
#     db.collection("orders").document(str(order_id)).set({
#         "from_address":from_address,
#         "to_address":to_address,
#         "price":price,
#         "from_lat":from_lat,
#         "from_lng":from_lng,
#         "to_lat":to_lat,
#         "to_lng":to_lng,
#         "visibilty":visibilty,
#         "status":"open",
#         "driver_id":None,
#         "order_id":str(order_id)

#         })

# def update_order_status_in_firebase(order_id,visibilty):
#     db.collection("orders").document(str(order_id)).update({
#         "visibilty":visibilty
#         })

# def create_order_in_firebase(order_id,from_address,to_address,price,from_lat,from_lng,to_lat,to_lng):

#     # Create order for 2km drivers = A category
#     set_order_in_firebase(order_id,from_address,to_address,price,from_lat,from_lng,to_lat,to_lng,"A")
#     print("Order with id = ",order_id, ' succesfully created in Firebase with status A')

#     # Wait 10 seconds and update order for 4km drivers = B category
#     time.sleep(10) 
#     update_order_status_in_firebase(order_id,"B")  
#     print("Order with id = ",order_id, ' status A changed to B')


#     # Wait 10 seconds and update order for all drivers = C category
#     time.sleep(10) 
#     update_order_status_in_firebase(order_id,"C")     
#     print("Order with id =  ",order_id, ' status B changed to C')


# def change_order_status(order_id,driver_id,status):
#     try:
#         db.collection("orders").document(str(order_id)).update({
#             "driver_id":driver_id,
#             "status":status,

#             })

#         return 200    

#     except:    
#         print("Some Exception")
#         return 500




# # create_order_in_firebase(777,"лондasdasdон","лондон","лондон","лондон","лондон")
# # print(attach_driver_to_order(4,77))
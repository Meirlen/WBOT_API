
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


db = firestore.client()



def set_order_in_firebase(order_id,price,route,visibilty,createdAt,is_share_trip,passenger_count,phone_number):
    db.collection("orders").document(str(order_id)).set({

        "price":price,
        "visibilty":visibilty,
        "status":"search_car",
        "driver_id":None,
        "order_id":str(order_id),
        "driver":{
            "lat":None,
            "lng":None
        },
        "route":route,
        "shareTrip":str(is_share_trip),
        "createdAt":str(createdAt),
        "passenger_count":str(passenger_count),
        "phone_number":str(phone_number)

        })

def update_order_status_in_firebase(order_id,status):
    print("update_order_status_in_firebase:",status)
    db.collection("orders").document(str(order_id)).update({
        "status":status
        })

def update_driver_location_in_firebase(order_id,lat,lng):
    print("update_driver_location_in_firebase:",str(lat),str(lng))
    db.collection("orders").document(str(order_id)).update({
        "driver":{
            "lat":str(lat),
            "lng":str(lng)
        }
        })

        
def update_order_visibilty_in_firebase(order_id,visibilty):
    db.collection("orders").document(str(order_id)).update({
        "visibilty":visibilty
        })

def update_order_visibilty_in_firebase(order_id,visibilty):
    db.collection("orders").document(str(order_id)).update({
        "visibilty":visibilty
        })


def create_order_in_firebase(order_id,price,route,createdAt,is_share_trip = None,passenger_count = None,phone_number = None):

    # Create order for 2km drivers = A category
    set_order_in_firebase(order_id,price,route,"A",createdAt,is_share_trip,passenger_count,phone_number)
    print("Order with id = ",order_id, ' succesfully created in Firebase with status A')

    # Wait 10 seconds and update order for 4km drivers = B category
    time.sleep(10) 
    update_order_visibilty_in_firebase(order_id,"B")  
    print("Order with id = ",order_id, ' status A changed to B')


    # Wait 10 seconds and update order for all drivers = C category
    time.sleep(10) 
    update_order_visibilty_in_firebase(order_id,"C")     
    print("Order with id =  ",order_id, ' status B changed to C')


def change_order_status(order_id,driver_id,status):
    try:
        db.collection("orders").document(str(order_id)).update({
            "driver_id":driver_id,
            "status":status,

            })

        return 200    

    except:    
        print("Some Exception")
        return 500





# FB PUSH 

import dataclasses
import json
import requests
from dataclasses import dataclass



@dataclass
class Notification:
    title:str
    body: str
    sound:str


@dataclass
class PushRequestBody:
    to:str
    notification: str 


@dataclass
class PushMultipleRequestBody:
    registration_ids:list
    notification: str 


def send_push_notification(token_to,title,body):
    fb_token = "AAAALypo7K8:APA91bEeOVuhcq1O4992uQP9ZpqY_Jp_izlHOAy4C85hUIIIZGzFuV1nlenbz0-Ah_WrcqqZW27byrvirHg0eZAqW-qcVj3bmDrnjmIC1I9ACSgvv-Pn8R00EV1iXXgHjS83F5JXLMt0"

    
    notification = Notification(title,body,"default")
    requestBody = PushRequestBody(token_to,notification)
    
    body = json.dumps(dataclasses.asdict(requestBody))



    response = requests.post(
            url='https://fcm.googleapis.com/fcm/send',
            headers={"Authorization":"key="+fb_token,"Content-Type":"application/json"},
            data=body
        ).json()

    print(response)  


def send_push_notification_to_multiple_devices(registration_ids,title,body):
    fb_token = "AAAALypo7K8:APA91bEeOVuhcq1O4992uQP9ZpqY_Jp_izlHOAy4C85hUIIIZGzFuV1nlenbz0-Ah_WrcqqZW27byrvirHg0eZAqW-qcVj3bmDrnjmIC1I9ACSgvv-Pn8R00EV1iXXgHjS83F5JXLMt0"

    
    notification = Notification(title,body,"default")
    requestBody = PushMultipleRequestBody(registration_ids,notification)
    
    body = json.dumps(dataclasses.asdict(requestBody))



    response = requests.post(
            url='https://fcm.googleapis.com/fcm/send',
            headers={"Authorization":"key="+fb_token,"Content-Type":"application/json"},
            data=body
        ).json()

    print(response)  




def update_driver_location_in_firebase(phone,lat,lon):
    db.collection("drivers").document(str(phone)).update({
        "lat":lat
        })  
# create_order_in_firebase(555,"500","route")
# print(attach_driver_to_order(4,77))
# to_token = "dZD_9UzgSSuI-QwqeN9j1z:APA91bG-uAT46KtS1O-VWTqAmpfkpdHQ2mxl1xbmp6l651ivUxZ9NGebCutBbYUMUoFnrxim4gPh1li7wnJZrCd0MSmcWwsZWF5G4pzCUur9m5BKakvoA4dMR29CtUYadsgBmBLTVbL2"
# send_push_notification(to_token,"💁 - К вам выехала машина.","Мазда серая 6666")

# registration_ids = ["feAeLVYvRJWdd59sx5SWc_:APA91bEhNVpQx7PkbdgGsX4LNRhXqy2xuxSoghYSQ9leEwSx1LWUwn0JCbwlkhgw0nYttg2iI9SPf4HRTUWGyAY6qPKTPMozFcjj926HiD3pDjGbRXMjEGFkFUlHZeaiu3VA9fVMSLzv"]
# send_push_notification_to_multiple_devices(registration_ids,"💁 - К вам выехала машина.","Мазда серая 6666")
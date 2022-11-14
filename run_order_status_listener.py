

import threading


def get_count():
    counter = 0

    threading.Timer(5.0, get_count).start()
    counter+=1
    records = get_records()
    print("Getting count...", str(records))


    return str(counter)

import random
def get_records():

    return random.randint(3, 9)

    
get_count()









import threading


def get_count():
    counter = 0

    threading.Timer(5.0, get_count).start()
    counter+=1
    records = counter
    print("Getting count...", str(records))


    return str(counter)

get_count()







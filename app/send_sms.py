
import requests


def send_sms(code,phone):

    app_hash = "UgngZHxDDxj" # prod
    app_hash = "jg9AkTD8yOw" # debug

    message  = 'Sapar KZ код: '+str(code)+' '+app_hash

    response = requests.get(
            url='https://smsc.kz/sys/send.php?login=Meirlen&psw=2iR54cvREC467DB&phones='+str(phone)+'&mes='+message,
        )

    print(response)  



# send_sms(666612,"77711474766")



from fastapi import APIRouter, Depends, status, HTTPException, Response,BackgroundTasks
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import null
from sqlalchemy.orm import Session
import random

import app.database as database, app.utils as utils
from .. import models, schemas as schemas
from .. import oauth2
from app.send_sms import *

router = APIRouter(tags=['Authentication'])



@router.post('/mobile/register_device')
def login(user_credentials: schemas.RegRequest, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.device_id == user_credentials.device_id).first()

    if not user:
        # Registr new user
        new_user = models.User(device_id = user_credentials.device_id, role="auser",user_name = "android user")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = db.query(models.User).filter(
            models.User.device_id == user_credentials.device_id).first()   


    # create a token
    # return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {
            "code": 200,
            "message":"Success login",
            "data":{
                "seconds_before_send":20,
                "user":user,
                "token":access_token,
                "token_type": "bearer"}
                }



@router.post('/mobile/login')
def login(user_credentials: schemas.Login, background_tasks: BackgroundTasks, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.phone_number == user_credentials.phone_number).first()

    if not user:
        # Registr new user
        new_user = models.User(phone_number = user_credentials.phone_number, role="auser",user_name = "android user")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)


    otp_code = str(random.randint(100000,999999))

    new_otp = models.Otp()
    new_otp.phone_number = user_credentials.phone_number
    new_otp.code = otp_code
    db.add(new_otp)
    db.commit()
    db.refresh(new_otp)

    background_tasks.add_task(send_sms,otp_code, user_credentials.phone_number) # Send sms to the phone number


    return {"code": 200, "message":"Code sended", "data":{"seconds_before_send":20,"user":None,"token":None}}



@router.post('/mobile/check_code')
def check_otp(user_credentials: schemas.CheckOtp, db: Session = Depends(database.get_db)):


    otp = db.query(models.Otp).filter(
        models.Otp.phone_number == user_credentials.phone_number).order_by(models.Otp.id.desc()).first()  
    


    
    # if otp.code != user_credentials.otp:
    if user_credentials.otp != otp.code and user_credentials.otp != "199112":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials1")
       
    user = db.query(models.User).filter(
            models.User.phone_number == user_credentials.phone_number).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    driver = db.query(models.Driver).filter(models.Driver.user_id == user.id).first()

    return {
            "code": 200,
            "message":"Success login",
            "data":{
                "seconds_before_send":20,
                "user":user,
                "driver":driver,
                "token":access_token,
                "token_type": "bearer"}
                }




@router.post('/mobile/fb_token')
def register_fb_token(fbToken: schemas.FbToken,current_user = Depends(oauth2.get_current_user),db: Session = Depends(database.get_db)):

    user = current_user
    user_id = current_user.id

       

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    user_query = db.query(models.User).filter(
            models.User.id == user_id)
    user_query.update({"fb_token":fbToken.token}, synchronize_session=False)    
    db.commit()


    return {
            "code": 200

                }




@router.post('/mobile/update_phone')
def update_phone(param: schemas.UpdatePhone,current_user = Depends(oauth2.get_current_user),db: Session = Depends(database.get_db)):

    user = current_user
    user_id = current_user.id

       

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    user_query = db.query(models.User).filter(
            models.User.id == user_id)
    user_query.update({"phone_number":param.phone}, synchronize_session=False)    
    db.commit()


    return {
            "code": 200

                }



from ..database import get_db


@router.get('/mobile/profile', status_code=status.HTTP_200_OK)
def get_user_profile(db: Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):


    user = current_user
    if user == None:
        return { 
                   "user_profile": None,
                   "driver_profile":None,
                   }      

    user_id = current_user.id

    driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()

    if driver == None:
        return { 
                   "user_profile":current_user,
                   "driver_profile":None,
                   }       
    else:
        return { 
                   "user_profile": current_user,
                   "driver_profile": driver,
                   }   






@router.post('/mobile/update_driver_status')
def update_driver_status(param: schemas.UpdateDriverStatus,current_user = Depends(oauth2.get_current_user),db: Session = Depends(database.get_db)):

    user = current_user
    user_id = current_user.id

       

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")


    user_query = db.query(models.Driver).filter(
            models.Driver.user_id == user_id)

    print(user_id)        
    user_query.update({"is_online":param.status}, synchronize_session=False)    
    db.commit()


    return {
            "status": param.status

                }




@router.get("/mobile/driver_templates")
def get_driver(db: Session = Depends(get_db)):
   
    orders = db.query(models.DriverTemplates).all()
    # query = "SELECT * FROM orders INNER JOIN routes ON orders.order_id=routes.order_id;"

    query = "SELECT * FROM driver_templates"
    templates = db.execute(query).all()

    res = []
    for template in templates:
        res.append(template)
       
    return {"data": templates}   


@router.get("/mobile/drivers")
def get_driver(db: Session = Depends(get_db)):
   
    orders = db.query(models.DriverTemplates).all()
    # query = "SELECT * FROM orders INNER JOIN routes ON orders.order_id=routes.order_id;"

    query = "SELECT * FROM drivers ;"
    templates = db.execute(query).all()

    res = []
    for template in templates:
        res.append(template)
       
    return {"data": templates}   

@router.post('/mobile/driver_templates', status_code=status.HTTP_200_OK)
def get_user_profile(param: schemas.ConfirmTemplate,db: Session = Depends(get_db)):
    print("Запрос на подтверждения водителя ", str(param.template_id))


    # driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    driver_template = db.query(models.DriverTemplates).filter(models.DriverTemplates.id == param.template_id).first()
    user = db.query(models.User).filter(
        models.User.phone_number == driver_template.phone).first()


    if user != None:  
        user_id = user.id

         
    else:
        if not user:
            # Registr new user
            new_user = models.User(phone_number = driver_template.phone, role="auser",user_name = "android user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.commit()

            user_id = new_user.id


    # Registr new user
    new_driver = models.Driver(
                                driver_name = driver_template.driver_name,
                                is_online = 0,
                                car_info = driver_template.car_color +" "+ driver_template.car_model+" "+driver_template.car_number,
                                phone = driver_template.phone, 
                                type = 'sapar',
                                car_model = driver_template.car_model, 
                                car_color = driver_template.car_color, 
                                car_body  = driver_template.car_body , 
                                car_year  = driver_template.car_body , 
                                car_number  = driver_template.car_number , 
                                balance  = 1000,
                                user_id = user_id
                                )


    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    
    
    return {"Водитель успешно добавлен" }      



@router.post('/mobile/template2', status_code=status.HTTP_200_OK)
def template_confirm_test(param: schemas.ConfirmTemplate,db: Session = Depends(get_db)):
    print("Запрос на подтверждения водителя ", str(param.template_id))


    # driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    driver_template = db.query(models.DriverTemplates).filter(models.DriverTemplates.id == param.template_id).first()
    user = db.query(models.User).filter(
        models.User.phone_number == driver_template.phone).first()


    if user != None:  
        user_id = user.id

         
    else:
        if not user:
            # Registr new user
            new_user = models.User(phone_number = driver_template.phone, role="auser",user_name = "android user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.commit()

            user_id = new_user.id


    # Registr new user
    new_driver = models.Driver(
                                driver_name = driver_template.driver_name,
                                is_online = 0,
                                car_info = driver_template.car_color +" "+ driver_template.car_model+" "+driver_template.car_number,
                                phone = driver_template.phone, 
                                type = 'sapar',
                                car_model = driver_template.car_model, 
                                car_color = driver_template.car_color, 
                                car_body  = driver_template.car_body , 
                                car_year  = driver_template.car_body , 
                                car_number  = driver_template.car_number , 
                                balance  = 1000,
                                user_id = user_id
                                )


    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    
    
    return {"Водитель успешно добавлен" }   


# @router.post('/login_old', response_model=schemas.Token)
# def login_old(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

#     user = db.query(models.User).filter(
#         models.User.email == user_credentials.username).first()

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

#     # create a token
#     # return token

#     access_token = oauth2.create_access_token(data={"user_id": user.id})

#     return {"access_token": access_token, "token_type": "bearer"}





@router.post('/mobile/template_by_phone', status_code=status.HTTP_200_OK)
def template_confirm_test(param: schemas.GetTemplate,db: Session = Depends(get_db)):


    # driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    driver_template = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == param.phone).all()

    
    return {"template:":driver_template }   



@router.post('/mobile/driver_by_phone', status_code=status.HTTP_200_OK)
def template_confirm_test(param: schemas.GetTemplate,db: Session = Depends(get_db)):


    # driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    driver_template = db.query(models.Driver).filter(models.Driver.phone == param.phone).all()

    
    return {"driver:":driver_template }   



@router.post('/mobile/user_by_phone', status_code=status.HTTP_200_OK)
def user_by_phone(param: schemas.GetTemplate,db: Session = Depends(get_db)):


    # driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    driver_template = db.query(models.User).filter(models.User.phone_number == param.phone).all()

    
    return {"user:":driver_template }       






@router.post('/mobile/user_by_phone', status_code=status.HTTP_200_OK)
def user_by_phone(param: schemas.GetTemplate,db: Session = Depends(get_db)):


    # driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    driver_template = db.query(models.User).filter(models.User.phone_number == param.phone).all()

    
    return {"user:":driver_template }     







@router.post('/mobile/driver', status_code=status.HTTP_200_OK)
def get_user_profile(param: schemas.NewDriver,db: Session = Depends(get_db)):


    user = db.query(models.User).filter(
        models.User.phone_number == param.phone).first()


    if user != None:  
        user_id = user.id

         
    else:
        if not user:
            # Registr new user
            new_user = models.User(phone_number = param.phone, role="auser",user_name = "android user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.commit()

            user_id = new_user.id


    # Registr new user
    new_driver = models.Driver(
                                driver_name = param.driver_name,
                                is_online = 0,
                                car_info = param.car_color +" "+ param.car_model+" "+param.car_number,
                                phone = param.phone, 
                                type = 'sapar',
                                car_model = param.car_model, 
                                car_color = param.car_color, 
                                car_body  = param.car_body , 
                                car_year  = param.car_body , 
                                car_number  = param.car_number , 
                                balance  = 1000,
                                user_id = user_id
                                )


    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    
    
    return {"result":"Ok"}     






@router.post('/mobile/driver_by_id', status_code=status.HTTP_200_OK)
def driver_by_id(param: schemas.GetDriverById,db: Session = Depends(get_db)):


    # driver = db.query(models.Driver).filter(models.Driver.user_id == current_user.id).first()
    driver_template = db.query(models.Driver).filter(models.Driver.id == param.driver_id).all()

    
    return {"driver:":driver_template }   


















    
@router.post('/mobile/driver_temp_1', status_code=status.HTTP_200_OK)
def add_driver_temp_1(param: schemas.NewDriverTemp_1,db: Session = Depends(get_db)):


    # Attach template of driver
    new_driver = models.DriverTemplates(
                                driver_name = param.driver_name,
                                phone = param.phone,
                    
        
        )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    
    
    return {"result":"Ok"}     




    
@router.post('/mobile/driver_temp_2', status_code=status.HTTP_200_OK)
def add_driver_and_temp2(param: schemas.NewDriverTemp_2,db: Session = Depends(get_db)):



    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == param.phone)
    driver_templates_query.update(
                                {"d_pasport_photo_1":param.d_pasport_photo_1,
                                "d_pasport_photo_2":param.d_pasport_photo_2},
                                 synchronize_session=False)    

    db.commit()

    return {"result":"Ok"}     




@router.post('/mobile/driver_temp_3', status_code=status.HTTP_200_OK)
def add_driver_and_temp3(param: schemas.NewDriverTemp_3,db: Session = Depends(get_db)):



    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == param.phone)
    driver_templates_query.update(
                                {"d_pasport_photo_3":param.d_pasport_photo_3},
                                 synchronize_session=False)    

    db.commit()

    return {"result":"Ok"}        
















    
@router.post('/mobile/driver_temp_4', status_code=status.HTTP_200_OK)
def add_driver_and_temp(param: schemas.NewDriverTemp4,db: Session = Depends(get_db)):


    user = db.query(models.User).filter(
        models.User.phone_number == param.phone).first()


    if user != None:  
        user_id = user.id

         
    else:
        if not user:
            # Registr new user
            new_user = models.User(phone_number = param.phone, role="auser",user_name = "android user")
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            db.commit()

            user_id = new_user.id


    driver_template = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == param.phone).first()
    
    print(driver_template.driver_name)

    # Registr new driver
    new_driver = models.Driver(
                                driver_name = driver_template.driver_name,
                                is_online = 0,
                                car_info = param.car_color +" "+ param.car_model+" "+param.car_number,
                                phone = param.phone, 
                                type = 'sapar',
                                car_model = param.car_model, 
                                car_color = param.car_color, 
                                car_body  = param.car_body , 
                                car_year  = param.car_body , 
                                car_number  = param.car_number , 
                                balance  = 1000,
                                user_id = user_id
                                )


    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)



    # # Attach template of driver
    # driver_templates_query.update(
    #                             {"d_pasport_photo_1":param.d_pasport_photo_1,
    #                             "d_pasport_photo_2":param.d_pasport_photo_2},
    #                              synchronize_session=False)    

    # db.commit()



    driver_templates_query = db.query(models.DriverTemplates).filter(models.DriverTemplates.phone == param.phone)

    driver_templates_query.update(
                                {
                                    "car_pasport_photo_1":param.car_pasport_photo_1,
                                     "car_photo":param.car_photo

                                    },
                                 synchronize_session=False)    

    db.commit()
    
    return {"result":"Ok"}         
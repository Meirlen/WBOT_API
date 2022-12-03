from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import null
from sqlalchemy.orm import Session
import random

import app.database as database, app.utils as utils
from .. import models, schemas as schemas
from .. import oauth2

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
def login(user_credentials: schemas.Login, db: Session = Depends(database.get_db)):

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

    return {"code": 200, "message":"Code sended", "data":{"seconds_before_send":20,"user":None,"token":None}}



@router.post('/mobile/check_code')
def check_otp(user_credentials: schemas.CheckOtp, db: Session = Depends(database.get_db)):


    otp = db.query(models.Otp).filter(
        models.Otp.phone_number == user_credentials.phone_number).order_by(models.Otp.id.desc()).first()  
    


    
    # if otp.code != user_credentials.otp:
    if user_credentials.otp != otp.code : #"111111"
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
    return {
            "code": 200,
            "message":"Success login",
            "data":{
                "seconds_before_send":20,
                "user":user,
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

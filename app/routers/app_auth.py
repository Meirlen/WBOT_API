from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import null
from sqlalchemy.orm import Session
import random

import app.database as database, app.utils as utils
from .. import models, schemas as schemas
from .. import oauth2

router = APIRouter(tags=['Authentication'])


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

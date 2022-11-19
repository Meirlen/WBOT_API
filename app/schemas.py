from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing import List




class OrderOut(BaseModel):
    title: str
    content: str


class YandexRoute(BaseModel):
        short_text:str
        geo_point:List[float]
        fullname:str
        type:str
        city:str

class OrderEstimate(BaseModel):
    route: List[YandexRoute]
    user_id: int


class OrderCreate(BaseModel):
    route: List[YandexRoute]
    user_id: int
    app_type:str
    tariff:str
    comment:str

class UpdateYToken(BaseModel):
    token:str
     
class OrderStatus(BaseModel):
    order_id: int
    status: str

class OrderDriverInfo(BaseModel):
    driver_name:str
    car_info:str
    price:str
    status: str
    user_phone:str

class DriverLocation(BaseModel):
    order_id: int

class Login(BaseModel):
    phone_number: str


class CheckOtp(BaseModel):
    phone_number: str
    otp: str



class UserCreate(BaseModel):
    email: EmailStr
    password: str    
    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



class WhatsappMessage(BaseModel):
    waId: str
    senderName: str   
    text:str 
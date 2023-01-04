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


class OrderCreate(BaseModel):
    route: List[YandexRoute]
    user_id: int
    app_type:str
    tariff:str
    comment:str

class UserOrderCreate(BaseModel):
    route: List[YandexRoute]
    app_type:str
    tariff:str
    comment:str

class UserOrderCreateNew(BaseModel):
    route: List[YandexRoute]
    tariff:str
    comment:str
    price:str
    is_share_trip:int
    passenger_count:int


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


class RegRequest(BaseModel):
    device_id: str

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

class FbToken(BaseModel):
    token: str


class UpdatePhone(BaseModel):
    phone: str


class UpdateDriverStatus(BaseModel):
    status: int


class ConfirmTemplate(BaseModel):
    template_id: int


class GetTemplate(BaseModel):
    phone: str

class TokenData(BaseModel):
    id: Optional[str] = None



class WhatsappMessage(BaseModel):
    waId: Optional[str] = None  
    senderName: Optional[str] = None 
    text:Optional[str] = None 
    type:Optional[str] = None 
    data:Optional[str] = None 
    user_id: Optional[int] = None



class GeoCodeRequest(BaseModel):
    lat: float
    lon:float    




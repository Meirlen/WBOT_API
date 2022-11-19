from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float,Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import List, Optional


from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String, nullable=False,server_default='search_car') 
    # search_car
    # assigned
    # arrived
    # expired
    # completed
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        "users.id"), nullable=True)

    yandex_order_id = Column(String)
    app_type = Column(String, nullable=False) 
    # y - yandex
    # b - baursak
    # r - region
    tariff = Column(String, nullable=False) 
    # c - Comfort
    # e - Econom

    # Driver location
    d_lat = Column(Float)
    d_lng = Column(Float)



class Credentials(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    value = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()')) 


    # csrf_token
    # 
    # 
    # 
    #                       

class Route(Base):
    __tablename__ = "routes"

    route_id = Column(Integer, primary_key=True, nullable=False)
    short_text = Column(String, nullable=False)
    fullname = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    city = Column(String, nullable=False)
    order_id = Column(Integer, ForeignKey(
        "orders.order_id"), nullable=True)

    # owner = relationship("Order")



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    user_name = Column(String, nullable=True)
    role = Column(String, nullable=False,server_default='user') # driver
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))



                
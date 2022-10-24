from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import List, Optional


from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String, nullable=False,server_default='open') 
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey(
        "users.id"), nullable=True)

    yandex_order_id = Column(String)

    # from_address = Column(String, nullable=False)
    # to_address = Column(String, nullable=False)
    # from_lat = Column(String, nullable=False)
    # from_lng = Column(String, nullable=False)
    # to_lat = Column(String, nullable=False)
    # to_lng = Column(String, nullable=False)
    # price =  Column(String, nullable=False)
    # Open - client created order
    # Assigned - diver assigned to order
    # Closed - order complted
   



    # owner = relationship("User")

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



class Otp(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, nullable=False)
    phone_number = Column(String, nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))                   
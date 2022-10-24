from tkinter.messagebox import NO
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter,BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas as schemas
from ..database import get_db
from .. import utils as utils
from .. import oauth2


router = APIRouter(
    prefix="/users",
    tags=['Users']
)
    
   
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user    
  


  
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user



@router.get('/driver/activity', status_code=status.HTTP_200_OK)
def get_driver_activity(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    active_order = db.query(models.Order).filter(models.Order.driver_id == current_user.id,models.Order.status != "completed" or models.Order.status != "open").first()
    if active_order == None:
       return {"order_id":None}

    return active_order

      
   
     
  
    
from fastapi import  status, HTTPException,Depends, APIRouter
from schemas import UserCreate, UserResponse
import models
from typing import List
from utils import hash
from database import get_db
from sqlalchemy.orm import Session

route = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

#CREATE USER
@route.post("/", status_code=status.HTTP_201_CREATED, response_model= UserResponse)
def create_user(user:UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user= models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return(new_user)

# GET USER DETAILS
@route.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")
    return user

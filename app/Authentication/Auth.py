from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from database import get_db
import models
import utils
import schemas
import OAuth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

route = APIRouter(
    tags=["Authentication"]
)

@route.post("/login", response_model= schemas.Token)
def login(usercredentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == usercredentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    plain_pass = usercredentials.password 
    hashed_password = user.password
    if not utils.verify(plain_pass, hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = OAuth2.create_access_token(data= {
        "user_id": user.id
    })

    return {"access_token": access_token, "token_type": "bearer" }

    


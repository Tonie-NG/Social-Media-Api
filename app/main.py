from fastapi import FastAPI
import models
from typing import List
from database import engine 
from Post import PostRoute
from User import UserRoute
from Vote import VoteRoute
from Authentication import Auth
from config import settings

print(settings.access_token_expiration_minutes)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()   

@app.get("/")
def root():
    return {"message": "Hello Tonie, Welcome to my API!"}

app.include_router(PostRoute.route)
app.include_router(UserRoute.route)
app.include_router(Auth.route)
app.include_router(VoteRoute.route)

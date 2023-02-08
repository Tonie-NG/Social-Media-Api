from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# declaring or defining pydanthic Schema. This is used to define the format of a client request or server response

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    class Config: 
        orm_mode = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    class Config: 
        orm_mode = True

class PostVote(BaseModel):
    Post: PostResponse
    likes: int
    class Config: 
        orm_mode = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
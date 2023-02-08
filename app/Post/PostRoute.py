from fastapi import status, HTTPException, Response, Depends, APIRouter
from fastapi.responses import JSONResponse
from schemas import PostBase, PostCreate, PostResponse, PostVote
import OAuth2
from typing import List
import models
from typing import List, Optional
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

route = APIRouter(
    prefix= "/posts",
    tags=["Posts"]
)

# Get all post of all users
# @route.get("/", status_code=status.HTTP_200_OK, response_model= List[PostResponse])
@route.get("/", status_code=status.HTTP_200_OK, response_model= List[PostVote])
def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user), 
    limit: int = 10, skip: int = 0, search: Optional[str] = '' 
):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

# createpost
@route.post("/", status_code = status.HTTP_201_CREATED, response_model= PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):

    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post) # used to add a resource
    db.commit() # used to commit a resource to our database
    db.refresh(new_post) #used to retrieve the resource created 
    return new_post

# getonepost
@route.get("/{id}",  status_code=status.HTTP_200_OK, response_model= PostVote)
def get_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found in the database")
       
    return post


#delete
@route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to do this")
        
    post_query.delete(synchronize_session = False)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Item not found"}) 


# Update
@route.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model= PostResponse)
def update_post(id: int, post:PostBase,  db: Session = Depends(get_db), current_user: int = Depends(OAuth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    posts = post_query.first()
    if posts == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with {id} was not found")
    
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to do this")

    post_query.update(post.dict(), synchronize_session = False)  
    db.commit()

    return post_query.first()

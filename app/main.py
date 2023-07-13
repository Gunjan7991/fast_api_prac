from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
from . import models
from .database import get_db, engine 
from .routers import posts

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(posts.router)

class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    


my_posts:list = [{"id": 1, "title": "Post1 ", "content": "Hello World", "published": True, "rating": 4}, {"id": 2, "title": "Post 2", "content": "My Name is slim shady.","published": True}, {"id": 3, "title": "Post 3", "content": "Hello from the other side!!", "published": False, "rating": 5}]


@app.get("/")
def root():
    return {"message": "Server is running..."}




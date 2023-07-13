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


@app.get("/posts")
def get_posts():
    return {"message": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: Post):
    print(type(post))
    post_id = my_posts[len(my_posts)-1]["id"]+1 
    post.id = post_id
    my_posts.append(post)
    return {"message": "Post Added!"}


@app.get("/posts/{id}")
def get_post_by_id(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {"message": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!" )

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post_by_id(id: int, post: Post):
    
    for n, posts in enumerate(my_posts):
        if posts["id"] == id:
            my_posts[n]["title"] = post.title
            my_posts[n]["content"] = post.content
            return {f"message {n}": my_posts[n]}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!" )

@app.delete("/posts/{id}")
def delete_post_by_id(id: int):
    for n, posts in enumerate(my_posts):
        if posts["id"] == id:
            my_posts.remove(posts)
            return {"message": "Post sucessfully removed!"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found!" )

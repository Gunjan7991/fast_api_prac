from fastapi import FastAPI, APIRouter
from . import models
from .database import engine 
from .routers import posts




# Creates all the table in database based on the models.
models.Base.metadata.create_all(bind=engine)


#Starter Code for Fastapi
app = FastAPI(title="FAST_API_PRAC",)
@app.get("/")
def status():
    return{"message": "Server running..."}


#include all the routes
app.include_router(posts.router)





from fastapi import FastAPI
from . import models, setting
from .database import engine
from .routers import posts, users, auth, likes, comments

# Creates all the table in database based on the models.
models.Base.metadata.create_all(bind=engine)

#importing logger setup
logger = setting.logger()

# Starter Code for Fastapi
app = FastAPI(title=setting.details["title"], summary=setting.details["summary"], description=setting.details["description"], version="1.0", openapi_tags=setting.tags_metadata)

# include all the routes
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(auth.router)



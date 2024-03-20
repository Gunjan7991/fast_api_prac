from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from . import models, setting
from .database import engine
from .routers import posts, users, auth, likes, comments

# Creates all the table in database based on the models.
models.Base.metadata.create_all(bind=engine)

# importing logger setup
logger = setting.logger()

# Starter Code for Fastapi
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title=setting.details["title"],
    summary=setting.details["summary"],
    description=setting.details["description"],
    version="1.0",
    openapi_tags=setting.tags_metadata,
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# include all the routes
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(auth.router)

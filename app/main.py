from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from sqladmin import Admin

from . import models, setting
from .database import engine
from .routers import posts, users, auth, likes, comments
from .admin import UserAdmin, PostAdmin, CommentAdmin
from .admin_auth import AdminAuth

# Creates all the tables in the database
models.Base.metadata.create_all(bind=engine)

# Logger
logger = setting.logger()

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# FastAPI app initialization
app = FastAPI(
    title=setting.details["title"],
    summary=setting.details["summary"],
    description=setting.details["description"],
    version="1.0",
    openapi_tags=setting.tags_metadata,
)

# CORS setup — use specific origins when allow_credentials=True
origins = [
    "http://localhost:3000",   # React/Frontend origin
    "http://127.0.0.1:3000",   # Alternate localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware required by SQLAdmin
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Add exception handler for rate limits
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# SQLAdmin dashboard setup
admin = Admin(
    app,
    engine,
    authentication_backend=AdminAuth(secret_key="super-secret-key")
)
admin.add_view(UserAdmin)
admin.add_view(PostAdmin)
admin.add_view(CommentAdmin)

# Register routers
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(likes.router)
app.include_router(comments.router)
app.include_router(auth.router)

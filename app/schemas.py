from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False


class PostCreate(PostBase):
    pass


class PostDisplay(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str]
    published: Optional[bool]

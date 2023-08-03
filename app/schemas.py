from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False


class PostCreate(PostBase):
    pass


class PostDisplay(PostBase):
    model_config = ConfigDict(from_attributes=True)


class PostUpdate(BaseModel):
    content: Optional[str]
    published: Optional[bool]


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str]


class UserCreate(UserBase):
    password: str
    re_password: str


class UserDisplay(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] | None = None
    email_verified: bool
    phone_verified: bool


class login(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    old_password: str
    phone: Optional[str]
    address: Optional[str]
    password: Optional[str]
    re_password: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
    name: Optional[str]

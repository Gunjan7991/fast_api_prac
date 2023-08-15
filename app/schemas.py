from pydantic import BaseModel, EmailStr, ConfigDict, constr
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = False


class PostCreate(PostBase):
    pass


class PostDisplay(PostBase):
    id: int


class PostUpdate(BaseModel):
    published: Optional[bool] = None


class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    address: Optional[str]


class UserCreate(UserBase):
    password: constr(min_length=10)
    re_password: str


class UserDisplay(BaseModel):
    id: int
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
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
    re_password: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
    name: Optional[str]


class vote(BaseModel):
    user_id: int
    post_id: int


class voter(BaseModel):
    user_id: int
    name: str


class comment(BaseModel):
    comment_id: int
    comment: str
    post_id: int
    user_id: int
    commentree: Optional[int]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BaseComment(BaseModel):
    comment: str
    post_id: int


class UpdateComment(BaseModel):
    comment: str


class AddComment(BaseComment):
    commentree: Optional[int] = None


class post_vote(PostDisplay):
    voteCount: int
    votes: list[voter]
    comments: list[comment]

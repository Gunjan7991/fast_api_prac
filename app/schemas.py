from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


def PostCreate(BaseModel):
    title: str
    content: str
    published: bool = False
    pass

def PostDisplay(BaseModel):
    pass


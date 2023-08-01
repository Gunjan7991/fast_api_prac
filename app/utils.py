from passlib.context import CryptContext
from . import schemas, models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def display_user(user: models.users) -> schemas.UserDisplay:
    usr = schemas.UserDisplay(address=user.address, email=user.email, phone=user.phone,
                              name=user.name, email_verified=user.email_verified if None else False,
                              phone_verified=user.phone_verified if None else False)
    return usr

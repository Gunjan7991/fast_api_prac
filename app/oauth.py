from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import logging
from .config import settings
from . import schemas, models
from .database import get_db
from .utils import display_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
logger = logging.getLogger(__name__)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=int(settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.secret_key,
                         algorithm=settings.algorithm)
    return encoded


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token=token, key=settings.secret_key,
                             algorithms=settings.algorithm)
        usr_id: str = payload.get("user_id")
        usr_name: str = payload.get("name")

        if usr_id is None:
            raise credentials_exceptions

        token_data = schemas.TokenData(id=str(usr_id), name=usr_name)

    except Exception as e:
        raise credentials_exceptions

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  detail="credentials not valid!", headers={"WWW-Authenticate: Bearer"})
    usr = models.users()
    try:
        token_data = verify_access_token(
            token=token, credentials_exceptions=credentials_exceptions)
        if token_data:
            user = db.query(models.users).filter(
                models.users.id == token_data.id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"User with id: {id} does not exist")

            usr = display_user(user)
            return usr
    except Exception as e:
        logger.warning(f"Exception Occured:")

    return usr

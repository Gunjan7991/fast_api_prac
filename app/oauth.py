from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now()+timedelta(minutes=int(settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.secret_key,
                         algorithm=settings.algorithm)
    return encoded


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token=token, key=settings.secret_key,
                             algorithms=settings.algorithm)

        id: str = payload.get("user_id")
        name: str = payload.get("name")

        if id is None:
            raise credentials_exceptions

        token_data = schemas.TokenData(id=id, name=name)

    except JWTError:
        raise credentials_exceptions


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  detail="credentials not valid!", headers={"WWW-Authenticate: Bearer"})
    return verify_access_token(token=token, credentials_exceptions=credentials_exceptions)

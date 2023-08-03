from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=int(settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.secret_key,
                         algorithm=settings.algorithm)
    return encoded


def verify_access_token(token: str, credentials_exceptions) -> schemas.TokenData:
    try:
        payload = jwt.decode(token=token, key=settings.secret_key,
                             algorithms=settings.algorithm)
        usr_id: str = payload.get("user_id")
        usr_name: str = payload.get("name")

        if usr_id is None:
            raise credentials_exceptions

        token_data = schemas.TokenData(id=str(usr_id), name=usr_name)
    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  detail="credentials not valid!", headers={"WWW-Authenticate: Bearer"})
    return verify_access_token(token=token, credentials_exceptions=credentials_exceptions)

from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import settings
from . import schemas


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
    

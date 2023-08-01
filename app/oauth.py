from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now()+timedelta(minutes=int(settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.secret_key,
                         algorithm=settings.algorithm)
    return encoded

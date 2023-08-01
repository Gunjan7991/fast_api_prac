from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import Settings


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now()+int(Settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, Settings.secret_key,
                         algorithm=Settings.algorithm)
    return encoded

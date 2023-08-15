from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import verify_password
from .. import schemas, models, oauth


router = APIRouter(prefix="/api/v1", tags=["Authentication"])
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/login", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Token
)
@limiter.limit("1/minute")
def login(
    request: Request,
    login_cred: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    logger.info(f"Request: {request.__dict__['scope']['client']}")
    user: models.users = (
        db.query(models.users).filter(models.users.email == login_cred.username).first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not verify_password(login_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    access_token = oauth.create_access_token(
        data={"user_id": user.id, "name": user.name}
    )

    return schemas.Token(access_token=access_token, token_type="Bearer")

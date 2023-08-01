from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import verify_password, display_user
from .. import schemas, models, oauth

router = APIRouter(prefix='/api/v1',
                   tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(login_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.users).filter(
        models.users.email == login_cred.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not verify_password(login_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    access_token = oauth.create_access_token(
        data={"user_id": user.id, "name": user.name})
    return {"message": "login sucessfull",
            "Token": {"access_token": access_token, "token_type": "bearer"},
            "Data": display_user(user)
            }

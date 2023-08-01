from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import verify_password, display_user
from .. import schemas, models

router = APIRouter(prefix='/api/v1',
                   tags=['Authentication'])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(login_cred: schemas.login, db: Session = Depends(get_db)):
    user = db.query(models.users).filter(
        models.users.email == login_cred.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not verify_password(login_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    return {"message": "login sucessfull",
            "Token": "Example Token",
            "Data": display_user(user)
            }

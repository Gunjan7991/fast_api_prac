from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import verify_password
from .. import schemas

router = APIRouter(prefix='/api/v1',
                   tags=['Authentication'])


router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(user: schemas.login, db:Session = Depends(get_db)):
    pass

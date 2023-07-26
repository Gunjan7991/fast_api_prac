from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas

router = APIRouter(prefix="/api/v1",
                   tags=["Users"])


@router.post("/users", status_code=status.HTTP_201_CREATED)
def save_users(users: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user: models.users = models.users(
        **users.model_dump(exclude="re_password"))
    if users.password == users.re_password:
        try:
            db.add(new_user)
            db.commit()

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                                detail=f"Exception Occured!! {e}")

        finally:
            return {"message": "Success!", "Data": new_user}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Password didn't Match")

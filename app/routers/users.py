from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..utils import hash, display_user


router = APIRouter(prefix="/api/v1",
                   tags=["Users"])


@router.post("/users", status_code=status.HTTP_201_CREATED)
def save_users(users: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user: models.users = models.users(
        **users.model_dump(exclude="re_password"))
    user_exits = db.query(models.users).filter(
        models.users.email == users.email).first()
    if user_exits:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email already Used.")

    user_exits = db.query(models.users).filter(
        models.users.phone == users.phone).first()

    if user_exits:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Phone Number already Used.")

    if users.password == users.re_password:
        new_user.password = hash(users.password)
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                                detail=f"Exception Occured!! {e}")

        finally:
            return {"message": "Success!", "Data": display_user(new_user)}

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Password didn't Match")


@router.get('/users/{id}', status_code=status.HTTP_200_OK)
async def get_user(id: int, db: Session = Depends(get_db),  current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Access Denied!! Unauthorized to access other's information!")

    user = db.query(models.users).filter(models.users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    usr = display_user(user)
    return usr

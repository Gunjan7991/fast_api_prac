from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas
from ..utils import hash, verify_password, display_user

router = APIRouter(prefix="/api/v1",
                   tags=["Users"])


@router.post("/users", status_code=status.HTTP_201_CREATED)
def save_users(users: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user: models.users = models.users(
        **users.model_dump(exclude="re_password"))

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
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.users).filter(models.users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    usr = display_user(user)
    return usr


@router.post('/users/login', status_code=status.HTTP_200_OK)
async def get_user_by_email(login: schemas.login, db: Session = Depends(get_db)):
    user = db.query(models.users).filter(
        models.users.email == login.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with Email does not exist!! Please Sign Up")
    if not verify_password(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"User with Email or Password didn't match!")
    usr = display_user(user)
    return {"Message": "Login Successful", "Detail": usr}


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.users).all()
        userList: list = []
        for user in users:
            userList.append(display_user(user))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")
    finally:
        return {"message": "Success!!", "Posts": userList}

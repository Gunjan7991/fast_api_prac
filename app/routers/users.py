from fastapi import APIRouter, HTTPException, status, Depends
import logging

from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..utils import hash, display_user, verify_password


router = APIRouter(prefix="/api/v1",
                   tags=["Users"])

logger = logging.getLogger(__name__)


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
def get_user(id: int, db: Session = Depends(get_db),  current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Access Denied!! Unauthorized to access other's information!")

    user = db.query(models.users).filter(models.users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    usr = display_user(user)
    return usr


@router.put("/users/update/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Access Denied!! Unauthorized to access other's information!")
    user_info = db.query(models.users).filter(models.users.id == id)
    user = user_info.first()
    update: bool = False
    if not verify_password(updated_user.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Authentication Failed")
    
    if not updated_user.address:
        logger.info("update function: address not passed")
        updated_user.address = user.address
    else:
        update = True
        
    if not updated_user.phone:
        logger.info("update function: phone not passed")
        updated_user.phone = user.phone
    else:
        update = True

    if not updated_user.password or not updated_user.re_password:
        logger.info("update function: password not passed")
        updated_user.password = user.password
    else:
        if updated_user.password == updated_user.re_password:
            updated_user.password = hash(updated_user.password)
            update = True
        else:
            raise HTTPException(
                status_code=status.HTTP_304_NOT_MODIFIED, detail="Password didn't match")
    message = {}
    if update:
        update = user_info.update(
            updated_user.model_dump(exclude=["re_password", "old_password"]), synchronize_session=False)
        logger.info(
            f"Update Status: {'Updated' if update == 1 else 'Not Updated'}")
        db.commit()
        user = db.query(models.users).filter(models.users.id == id).first()
        message = {"Message": "Updated", "User_Info": display_user(user)}
    else:
        message = {"Message": "Not_Updated", "User_Info": display_user(user)}
    return message

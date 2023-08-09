from fastapi import APIRouter, HTTPException, status, Depends
import logging
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth


router = APIRouter(prefix="/api/v1",
                   tags=["Posts"])

logger = logging.getLogger(__name__)


@router.get("/posts", status_code=status.HTTP_200_OK)
async def get_post(db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    if not get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Login to Modify")
    try:
        my_posts = db.query(models.posts).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")
    finally:
        posts = []
        for post in my_posts:

            if post.published or post.owner_id == int(get_current_user.id):
                posts.append(post)
        return posts


@router.get("/posts/my", status_code=status.HTTP_200_OK, )
def get_post_by_me(db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    if not get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Login to Modify")
    my_posts = db.query(models.posts).filter(
        models.posts.owner_id == get_current_user.id).all()
    if my_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return my_posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostDisplay)
def save_post(posts: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    if not get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Login to Modify")
    new_post = models.posts(owner_id=int(
        get_current_user.id), **posts.model_dump())
    try:
        db.add(new_post)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")
    finally:
        return new_post


@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostDisplay)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    if not get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Login to Modify")
    post_query = db.query(models.posts).filter(models.posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post with id: {id} found!")
    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to Modify this Post!")

    update = post_query.update(
        updated_post.model_dump(), synchronize_session=False)
    logger.info(
        f"Update Status: {'Updated' if update == 1 else 'Not Updated'}")
    db.commit()
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: schemas.UserDisplay = Depends(oauth.get_current_user)):
    if not get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Login to Modify")

    post_query = db.query(models.posts).filter(models.posts.id == id)
    post: models.posts = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post with id: {id} found!")

    if post.owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not Authorized to Modify this Post!")

    deletes = post_query.delete(synchronize_session=False)
    db.commit()
    if deletes != 1:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!!")

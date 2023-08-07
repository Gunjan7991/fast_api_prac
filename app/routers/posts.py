from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth

router = APIRouter(prefix="/api/v1",
                   tags=["Posts"])


@router.get("/posts", status_code=status.HTTP_200_OK, response_model=schemas.PostDisplay)
async def get_post(db: Session = Depends(get_db)):
    try:
        my_posts = db.query(models.posts).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")
    finally:
        return my_posts


@router.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostDisplay)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    try:
        my_posts = db.query(models.posts).filter(models.posts.id == id).first()
        if my_posts == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")
    finally:
        return my_posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostDisplay)
def save_post(posts: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: schemas.TokenData = Depends(oauth.get_current_user)):

    print(
        f"TokenData: {get_current_user}")  # , id: {get_current_user.id}, name: {get_current_user.name}
    new_post = models.posts(owner_id=int(
        get_current_user.id), **posts.model_dump())
    try:
        db.add(new_post)
        db.commit()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")

    finally:
        return posts


@router.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostDisplay)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    try:
        post_query = db.query(models.posts).filter(models.posts.id == id)
        post = post_query.first()
        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Post with id: {id} found!")

        post_query.update(updated_post.model_dump(), synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")
    finally:
        return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    try:
        post_query = db.query(models.posts).filter(models.posts.id == id)
        post = post_query.first()
        if post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"No Post with id: {id} found!")
        post_query.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")
    finally:
        return {"message": "Deletion Sucess!"}

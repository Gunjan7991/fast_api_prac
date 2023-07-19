from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas

router = APIRouter(prefix="/api/v1",
                   tags=["Posts"])


@router.get("/posts")
async def get_post(db: Session = Depends(get_db)):
    my_posts = db.query(models.posts).all()
    return {"message": "Success!!", "Posts": my_posts}


@router.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    my_posts = db.query(models.posts).filter(models.posts.id == id).first()
    return {"message": "Success!!", "Post": my_posts}


@router.post("/posts")
def save_post(posts: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.posts(**posts.dict())
    try:
        db.add(new_post)
        db.commit()
    except Exception as e:
        return {"message": e}
    return {"message": posts}


@router.put("/posts/{id}")
def update_post(id: int, posts: schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.posts).filter(models.posts.id == id).first()
    if post_query == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post with id: {id} found!")

from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import posts

router = APIRouter(prefix="/api/v1",
                   tags=["Posts"])


@router.get("/posting")
async def get_post(db: Session = Depends(get_db)):
    my_posts = db.query(posts).all()
    return {"message": "Success!!", "Posts": my_posts}


@router.get("/posts/{id}")
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    my_posts = db.query(posts).filter(posts.id == id).first()
    return {"message": "Success!!", "Post": my_posts}

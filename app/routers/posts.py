from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import posts

router = APIRouter(prefix="/api/v1",
                   tags=["Posts"])


@router.get("/posting")
async def get_post(db: Session = Depends(get_db)):
    my_posts = db.query(posts).all()
    print(type(my_posts))
    print(my_posts[0])
    return {"message": "Success!!", "Posts": my_posts}

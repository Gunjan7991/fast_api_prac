from fastapi import APIRouter, Depends, HTTPException, status
import logging
from sqlalchemy.orm import Session

from ..database import get_db
from ..oauth import get_current_user
from .. import schemas, models


router = APIRouter(prefix="/api/v1",
                   tags=["Votes"])

logger = logging.getLogger(__name__)


@router.post("/votes/{post_id}", status_code=status.HTTP_201_CREATED)
def add_vote(post_id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(get_current_user)):
    user_id = current_user.id
    post = db.query(models.posts).filter(models.posts.id == post_id).first()
    logger.debug(f"Posts Found!!")
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Posts with post_id: {post_id} found")
    like = schemas.vote(user_id=user_id, post_id=post_id)
    new_vote = models.votes(**like.model_dump())
    try:
        db.add(new_vote)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")


@router.delete("/votes/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_vote(post_id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(get_current_user)):
    vote_query = db.query(models.votes).filter(
        models.votes.user_id == current_user.id and  models.votes.post_id == post_id)
    vote = vote_query.first()
    if not vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No vote with post_id: {post_id} found")
    try:
        vote_query.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,
                            detail=f"Exception Occured!! {e}")

from fastapi import APIRouter, HTTPException, status, Depends
import logging
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, oauth

router = APIRouter(prefix="/api/v1", tags=["Comments"])
logger = logging.getLogger(__name__)

@router.post("/comments", status_code=status.HTTP_201_CREATED, response_model=schemas.comment)
def add_comment(comment:schemas.AddComment, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    user_id = current_user.id
    post = db.query(models.posts).filter(models.posts.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id: {comment.post_id}")
    
    new_comment = models.comments(user_id = user_id, **comment.model_dump())
    db.add(new_comment)
    db.commit()
    logger.info(f"comment: {new_comment.comment_id, new_comment.comment, new_comment.user_id, new_comment.post_id, new_comment.commentree, new_comment.created_at}")
    return schemas.comment.model_validate(new_comment)

@router.put("/comments/{comment_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.comment)
def update_comment(comment_id: int, comment:schemas.UpdateComment, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    comment_query = db.query(models.comments).filter(models.comments.comment_id == comment_id)
    my_comment: models.comments = comment_query.first()
    if not my_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comment with id: {comment_id} found!")
    
    if my_comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User can only modify thier comments!!")
    
    
    update = comment_query.update({"comment": comment.comment})
    logger.info(
        f"Update Status: {'Updated' if update == 1 else 'Not Updated'}")
    db.commit()
    db.refresh(my_comment)
    logger.info(f"comment: {type(my_comment), my_comment.comment_id, my_comment.comment, my_comment.user_id, my_comment.post_id, my_comment.commentree, my_comment.created_at}")
    return schemas.comment.model_validate(my_comment)

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth.get_current_user)):
    comment_query = db.query(models.comments).filter(models.comments.comment_id == comment_id)
    my_comment = comment_query.first()
    if not my_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No comment with id: {comment_id} found!")
    
    if my_comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User can only modify thier comments!!")
    
    update = comment_query.delete(synchronize_session=False)
    logger.info(
        f"Update Status: {'Updated' if update == 1 else 'Not Updated'}")
    db.commit()
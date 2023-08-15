from fastapi import APIRouter, HTTPException, status, Depends, Request
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .. import models, schemas, oauth


router = APIRouter(prefix="/api/v1", tags=["Posts"])
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)


@router.get("/posts", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_post(
    request: Request,
    db: Session = Depends(get_db),
    get_current_user: schemas.TokenData = Depends(oauth.get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    if not get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login to Modify"
        )

    my_posts = (
        db.query(models.posts)
        .filter(
            or_(
                models.posts.published == True,
                models.posts.owner_id == int(get_current_user.id),
            )
        )
        .limit(limit)
        .offset(skip)
        .all()
    )
    if not my_posts:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED)
    posts = []

    for post in my_posts:
        votes = db.query(models.votes).filter(models.votes.post_id == post.id).all()
        logger.debug(f"Print(votes): {votes}")
        count = len(votes)
        voters = []
        for vote in votes:
            voting_user_info = (
                db.query(models.users).filter(models.users.id == vote.user_id).first()
            )
            voters.append(
                schemas.voter(user_id=vote.user_id, name=voting_user_info.name)
            )
        comments = (
            db.query(models.comments).filter(models.comments.post_id == post.id).all()
        )
        pd = schemas.post_vote(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            voteCount=count,
            votes=voters,
            comments=comments,
        )
        posts.append(pd)
    return posts


@router.get(
    "/posts/my",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_post_by_me(
    request: Request,
    db: Session = Depends(get_db),
    get_current_user: schemas.TokenData = Depends(oauth.get_current_user),
):
    if not get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login to Modify"
        )
    my_posts = (
        db.query(models.posts)
        .filter(models.posts.owner_id == get_current_user.id)
        .all()
    )
    if my_posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    posts = []
    for post in my_posts:
        votes = db.query(models.votes).filter(models.votes.post_id == post.id).all()
        logger.debug(f"Print(votes): {votes}")
        count = len(votes)
        voters = []
        for vote in votes:
            voting_user_info = (
                db.query(models.users).filter(models.users.id == vote.user_id).first()
            )
            voters.append(schemas.voter(vote.user_id, voting_user_info.name))
        comments = (
            db.query(models.comments).filter(models.comments.post_id == post.id).all()
        )
        pd = schemas.post_vote(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            voteCount=count,
            votes=voters,
            comments=comments,
        )
        posts.append(pd)
    return posts


@router.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostDisplay
)
@limiter.limit("10/minute")
def save_post(
    request: Request,
    posts: schemas.PostCreate,
    db: Session = Depends(get_db),
    get_current_user: schemas.TokenData = Depends(oauth.get_current_user),
):
    if not get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login to Modify"
        )
    new_post = models.posts(owner_id=int(get_current_user.id), **posts.model_dump())
    try:
        db.add(new_post)
        db.commit()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail=f"Exception Occured!! {e}",
        )
    finally:
        return new_post


@router.put(
    "/posts/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.PostDisplay,
)
@limiter.limit("10/minute")
def update_post(
    request: Request,
    id: int,
    updated_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    get_current_user: schemas.TokenData = Depends(oauth.get_current_user),
):
    if not get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login to Modify"
        )
    post_query = db.query(models.posts).filter(models.posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Post with id: {id} found!",
        )
    if post.owner_id != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not Authorized to Modify this Post!",
        )

    update = post_query.update(updated_post.model_dump(), synchronize_session=False)
    logger.info(f"Update Status: {'Updated' if update == 1 else 'Not Updated'}")
    db.commit()
    return post


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/minute")
def delete_post(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    get_current_user: schemas.UserDisplay = Depends(oauth.get_current_user),
):
    if not get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Login to Modify"
        )

    post_query = db.query(models.posts).filter(models.posts.id == id)
    post: models.posts = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Post with id: {id} found!",
        )

    if post.owner_id != get_current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Not Authorized to Modify this Post!",
        )

    deletes = post_query.delete(synchronize_session=False)
    db.commit()
    if deletes != 1:
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail=f"Exception Occured!!",
        )

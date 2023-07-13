from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix= "/api/v1",
                   tags = ["Posts"])

@router.get("/posts")
async def get_post(db: Session = Depends(get_db)):
    return {"message": "Success!!"}
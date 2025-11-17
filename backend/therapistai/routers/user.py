from fastapi import APIRouter, Depends
from therapistai.db.models import User
from therapistai.db import get_session
from sqlmodel import Session
from pydantic import BaseModel
router = APIRouter()

class UserRequest(BaseModel):
    firstName: str 
    lastName: str 
    email: str

@router.post("/user/", tags=["user"])
async def user(user_req:UserRequest, session: Session = Depends(get_session)):
    user = User(firstName=user_req.firstName, lastname=user_req.lastName, email=user_req.email) 
    session.add(user)
    session.commit()
    session.refresh(user)
    return [user]
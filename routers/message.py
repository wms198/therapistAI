from fastapi import APIRouter, Depends
from db.models import Message
from db import get_session
import ai

from pydantic import BaseModel
from sqlmodel import Session, select
router = APIRouter()

class MessageRequest(BaseModel):
    content:str
    user_id: int



@router.post("/message/", tags=["message"])
async def create_message(msg:MessageRequest, session: Session = Depends(get_session)):
    user_m = Message(role="user", content=msg.content, user_id=msg.user_id) 
    session.add(user_m)
    session.commit()
    session.refresh(user_m)
    
    query = select(Message).where(Message.role == 'user')
    all_messages = session.exec(query).all()
    prediction = ai.chat(all_messages)
    ai_m = Message(role='llm', content=prediction.content)
    session.add(ai_m)
    session.commit()
    session.refresh(user_m)
    session.refresh(ai_m)
    return [user_m, ai_m]

@router.get("/message/", tags=["message"])
async def get_message(session: Session = Depends(get_session)):
    query = select(Message)
    all_messages = session.exec(query).all()
    return all_messages
    

@router.get("/replay", tags=["message"])
async def replay(session: Session = Depends(get_session)):
    query = select(Message).where(Message.role == 'user')
    all_messages = session.exec(query).all()
    prediction = ai.chat(all_messages)
    ai_m = Message(role='llm', content=prediction.content)
    return ai_m
    
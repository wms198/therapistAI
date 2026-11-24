from therapistai.db.models import Message
from therapistai.db.models import User
from therapistai.db import get_session
from therapistai import ai
from therapistai.auth import auth

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
router = APIRouter()

class MessageRequest(BaseModel):
    content: str

@router.post("/message/", tags=["message"])
async def create_message_route(msg: MessageRequest, session: Session = Depends(get_session), user = Depends(auth)):
    return create_message(
        session,
        user,
        msg.content,
    )


async def create_message(session: Session, user: User, message_content: Message):
    user_message = Message(role="user", content=message_content, user_id=user.id)
    session.add(user_message)
    session.commit()
    session.refresh(user_message)
    
    query = select(Message).where(Message.role == 'user', Message.user_id == user.id)
    all_messages = session.exec(query).all()
    prediction = ai.chat(all_messages)
    ai_m = Message(role='llm', content=prediction.content, user_id=user.id)
    session.add(ai_m)
    session.commit()
    session.refresh(user_message)
    session.refresh(ai_m)
    return [user_message, ai_m]

@router.get("/message/", tags=["message"])
async def get_message(session: Session = Depends(get_session), user = Depends(auth)):
    query = select(Message).filter_by(user_id=user.id)
    all_messages = session.exec(query).all()
    return all_messages
    

@router.get("/replay", tags=["message"])
async def replay(session: Session = Depends(get_session)):
    query = select(Message).where(Message.role == 'user')
    all_messages = session.exec(query).all()
    prediction = ai.chat(all_messages)
    ai_m = Message(role='llm', content=prediction.content)
    return ai_m
    
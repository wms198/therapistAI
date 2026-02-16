import os
from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlmodel import Session
from therapistai.auth import verify_password, create_access_token
from therapistai.db import get_session
from therapistai.db.models import User
from datetime import timedelta
router = APIRouter()

SECRET = os.getenv('JWT_SECRET')
class Login(BaseModel):
    email: str
    password: str


@router.post("/auth", tags=["login"])
async def get_jwt_from_pw(
    login_req: Login, response: Response, session: Session = Depends(get_session)
):
    stmt = select(User).filter(User.email == login_req.email)
    user: User | None = session.scalars(stmt).first()
    if user is not None and verify_password(login_req.password, user.password):
        access_token = create_access_token(
            user_id=user.id,
            expire_delta=timedelta(hours=12),
            first_name=user.firstName,
            aud="api",
        )
        refresh_token = create_access_token(
            user_id=user.id,
            expire_delta=timedelta(days=7),
            aud="refresh"
        )
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return {"error": "invalid credentials"}

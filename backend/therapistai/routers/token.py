import os
from typing import Annotated
from fastapi import APIRouter, Depends, Response, status, Form
from fastapi.responses import RedirectResponse
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

def _get_tokens(db, email:str, password:str) -> dict[str, str] | None:
    stmt = select(User).filter(User.email == email)
    user: User | None = db.scalars(stmt).first()
    if user is not None and verify_password(password, user.password):
        access_token, expires_at = create_access_token(
            user_id=user.id,
            expire_delta=timedelta(hours=12),
            first_name=user.firstName,
            aud="api",
        )
        refresh_token, rf_expires = create_access_token(
            user_id=user.id,
            expire_delta=timedelta(days=7),
            aud="refresh"
        )
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expries_at': expires_at,
            'refresh_token_expries_at': rf_expires,
        }

@router.post("/login")
async def login(
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: Session = Depends(get_session),
):
    tokens = _get_tokens(db, email, password)
    if not tokens:
        return RedirectResponse("http://localhost:5173/?error=wrong_password", status_code=status.HTTP_302_FOUND)
    response = RedirectResponse("http://localhost:5173/dashboard", status_code=status.HTTP_302_FOUND)

    response.set_cookie(
        key="access_token",
        value=tokens['access_token'],
        expires=tokens['access_token_expries_at'],
        domain="localhost"
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens['refresh_token'],
        expires=tokens['refresh_token_expries_at'],
        httponly=True,
        domain="localhost",
    )
    return response

@router.post("/auth", tags=["login"])
async def get_jwt_from_pw(
    login_req: Login, response: Response, session: Session = Depends(get_session)
):
    tokens = _get_tokens(session, login_req.email, login_req.password)
    if tokens:
        return tokens

    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return {"error": "invalid credentials"}

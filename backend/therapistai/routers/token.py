from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlmodel import Session
from therapistai.auth import verify_password
from therapistai.db import get_session
from therapistai.db.models import User

router = APIRouter()


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
        return "generate a JWT here"

    response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return {"error": "invalid credentials"}

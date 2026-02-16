import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException, status
from pwdlib import PasswordHash
from pydantic import BaseModel
from therapistai.db import Session, get_session
from therapistai.db.models import User

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

UNAUTHORIZED_EXP = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Must login")

class Token(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def create_access_token(
    user_id: int,
    expire_delta: timedelta,
    **claims,
):
    encode = {
        "sub": str(user_id),
        "exp": datetime.now(tz=timezone.utc) + expire_delta,
        **claims,
    }
    return jwt.encode(encode, JWT_SECRET, algorithm=ALGORITHM)


def decode(token: str, audience: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[ALGORITHM],
        audience=audience,
        options={"require": ["exp", "sub"]},
    )


async def auth(
    authorization: Annotated[str | None, Header()] = None,
    session: Session = Depends(get_session),
):
    if authorization is None:
        raise UNAUTHORIZED_EXP
    type_, middle, token   = authorization.partition(' ')
    if type_ != "Bearer" or middle != " ":
        raise UNAUTHORIZED_EXP
    try:
        claims = decode(token, "api")
    except jwt.DecodeError:
        raise UNAUTHORIZED_EXP

    user = session.get(User, claims["sub"])
    if user is None:
        raise UNAUTHORIZED_EXP
    return user

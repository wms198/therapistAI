from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import exc, select
from sqlmodel import Session
from therapistai.auth import UNAUTHORIZED_EXP, get_password_hash, auth
from therapistai.db import get_session
from therapistai.db.models import User

router = APIRouter()


# CRUD: https://www.geeksforgeeks.org/python/fastapi-crud-operations/
class UserRequest(BaseModel):
    firstName: str
    lastName: str
    email: str
    emailProvider: str
    password: str


class UserUpdate(BaseModel):
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None
    emailProvider: str | None = None
    password: str | None = None


@router.post("/user/", tags=["user"], status_code=status.HTTP_201_CREATED)
async def create_user(
    user_req: UserRequest, response: Response, session: Session = Depends(get_session)
):
    user = User(
        firstName=user_req.firstName,
        lastName=user_req.lastName,
        email=user_req.email,
        emailProvider=user_req.emailProvider,
        password=get_password_hash(user_req.password),
    )
    session.add(user)
    try:
        session.commit()
    except exc.IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "User with the email already exists"}
    session.refresh(user)
    return user


@router.get("/user/", tags=["user"])
async def getusers(session: Session = Depends(get_session)):
    stmt = select(User).order_by(User.id)
    return session.scalars(stmt).all()

@router.get("/user/me", tags=["user"])
async def me(user=Depends(auth)):
    return user

@router.get("/user/{id_}", tags=["user"])
async def getUser(id_: int, session: Session = Depends(get_session)):
    user = session.get(User, id_)
    return user


@router.put("/user/{id_}")
async def updateUser(
    id_: int,
    user_req: UserUpdate,
    response: Response,
    session: Session = Depends(get_session),
    user=Depends(auth),
):
    if id_ != user.id:
        raise UNAUTHORIZED_EXP
    for field_name in user_req.model_fields_set:
        if (value := getattr(user_req, field_name)) is not None:
            setattr(user, field_name, value)
    try:
        session.commit()
    except exc.IntegrityError:
        response.status_code = status.HTTP_409_CONFLICT
        return {"error": "User with the email already exists"}
    session.refresh(user)
    return user


@router.delete("/user/{id_}")
async def deleteUser(id_: int, session: Session = Depends(get_session)):
    user = session.get(User, id_)
    session.delete(user)
    session.commit()
    return {"message": "Item deleted successfully"}

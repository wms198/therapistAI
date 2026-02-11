from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel
from sqlalchemy import exc, select
from sqlmodel import Session

from therapistai.db import get_session
from therapistai.db.models import User
from therapistai.auth import get_password_hash

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
# @router.get("/", status_code=status.HTTP_201_CREATED)
async def createUser(
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
# @router.get("/")
async def getusers(session: Session = Depends(get_session)):
    stmt = select(User).order_by(User.id)
    return session.scalars(stmt).all()


@router.get("/user/{id}", tags=["user"])
async def getUser(id: str, session: Session = Depends(get_session)):
    user = session.get(User, id)
    return user


@router.put("/user/{id}")
async def updateUser(
    id: str,
    user_req: UserUpdate,
    response: Response,
    session: Session = Depends(get_session),
):
    user = session.get(User, id)
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


@router.delete("/user/{id}")
async def deleteUser(id: int, session: Session = Depends(get_session)):
    user = session.get(User, id)
    session.delete(user)
    session.commit()
    return {"message": "Item deleted successfully"}

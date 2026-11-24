from contextlib import asynccontextmanager
import asyncio
from therapistai.automation import check_loop
from sqlmodel import SQLModel
from therapistai.db import engine
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from therapistai.routers import message, appointment, user, token
from therapistai.auth import auth
from therapistai.db import get_session
import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)
@sio.on
def ping(sid, data):
    print('did a ping!')
    print('ping', sid, data)

@sio.event
async def userContent(sid, data):
    with next(get_session()) as session:
        user = await auth(access_token=data['access_token'], session=session)
        response = await message.create_message(
            session = session,
            user = user,
            message_content = data['userContent'],
        )
    print(f"response received: {response}")




@asynccontextmanager
async def lifespan(app: FastAPI):
    # https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#create-the-engine
    print("creating tables")
    SQLModel.metadata.create_all(engine)
    print("db is connecting")
    asyncio.create_task(check_loop())
    yield
    print("shutting down")

# https://fastapi.tiangolo.com/advanced/events/
app = FastAPI(lifespan=lifespan)
combined_app = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=app
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(message.router)
app.include_router(appointment.router)
app.include_router(user.router)
app.include_router(token.router)
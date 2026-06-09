from contextlib import asynccontextmanager
import asyncio
from therapistai.automation import check_loop
from sqlmodel import SQLModel
from therapistai.db import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from therapistai.routers import message, appointment, user, token
import socketio

# https://github.com/miguelgrinberg/python-socketio/blob/main/examples/server/asgi/fastapi-fiddle.py
# https://github.com/BimaAdi/fastapi-with-python-socketio-example/blob/main/main.py
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)
@sio.on
def ping(sid, data):
    print('did a ping!')
    print('ping', sid, data)

@sio.on('messager')
def userMessage(sid, data):
    pass

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
from contextlib import asynccontextmanager
import asyncio
from automation import check_loop
from sqlmodel import SQLModel
from db import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import message, appointment
from db import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#create-the-engine
    SQLModel.metadata.create_all(engine)
    print("db is connecting")
    asyncio.create_task(check_loop())
    yield

# https://fastapi.tiangolo.com/advanced/events/
app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message.router)
app.include_router(appointment.router)


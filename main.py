from contextlib import asynccontextmanager
import asyncio
from automation import check_loop
from sqlmodel import SQLModel
from db import engine
from fastapi import FastAPI
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
app.include_router(message.router)
app.include_router(appointment.router)




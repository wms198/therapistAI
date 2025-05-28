from sqlalchemy import create_engine
from db.models import *
from sqlmodel import Session
from contextlib import contextmanager

engine = create_engine('postgresql+psycopg2://postgres:admin123@localhost:54321/therapistai')

def get_session():
    with Session(engine) as session:
        yield session
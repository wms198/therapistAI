from sqlalchemy import create_engine
from sqlmodel import Session

# https://www.geeksforgeeks.org/python/fastapi-crud-operations/
engine = create_engine('postgresql+psycopg2://postgres:admin123@localhost:54321/therapistai')

def get_session():
    with Session(engine) as session:
        yield session
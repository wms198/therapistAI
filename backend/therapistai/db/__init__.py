import os
from sqlalchemy import create_engine
from sqlmodel import Session

# https://www.geeksforgeeks.org/python/fastapi-crud-operations/
engine = create_engine(os.getenv("DATABASE_URL"))
print(f"DATABASE_URL: {len(os.getenv('DATABASE_URL'))}")

def get_session():
    with Session(engine) as session:
        yield session
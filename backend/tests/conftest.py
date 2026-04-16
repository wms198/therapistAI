import os
import pytest

SQLITE_LOCATION = 'test.sqlite'
JWT_SECRET_MOCK = "Lz4GPC7bJHr8fAYQKc"
DB_URL = f'sqlite:///{SQLITE_LOCATION}'
os.environ["JWT_SECRET"] = JWT_SECRET_MOCK
os.environ["DB_URL"] = DB_URL

from therapistai.db import engine

@pytest.fixture(autouse=True)
def clean_db():
    # https://docs.sqlalchemy.org/en/21/core/connections.html#engine-disposal
    engine.dispose()
    if os.path.isfile(SQLITE_LOCATION):
        os.remove(SQLITE_LOCATION)
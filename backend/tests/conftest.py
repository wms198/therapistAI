import os

import pytest

SQLITE_LOCATION = 'test.sqlite'
JWT_SECRET_MOCK = "Lz4GPC7bJHr8fAYQKc"
DB_URL = f'sqlite:///{SQLITE_LOCATION}'
os.environ["JWT_SECRET"] =  JWT_SECRET_MOCK
os.environ["DB_URL"] = DB_URL

@pytest.fixture(scope='function', autouse=True)
def clean_db():
    if os.path.isfile(SQLITE_LOCATION):
        os.remove(SQLITE_LOCATION)
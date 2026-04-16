import jwt
from therapistai import auth
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from .conftest import JWT_SECRET_MOCK

ALGORITHM = "HS256"
def test_get_password_hash():
    password_hash = PasswordHash.recommended()
    password = '323433'
    hash = auth.get_password_hash(password)

    assert password_hash.verify(password, hash)

def test_create_access_token():
    user_id = 123
    expire_delta = timedelta(minutes=30) 
    token, _ = auth.create_access_token(user_id, expire_delta)
    print(token)
    # https://pyjwt.readthedocs.io/en/stable/usage.html#encoding-decoding-tokens-with-hs256
    decode = jwt.decode(token, JWT_SECRET_MOCK, ALGORITHM)

    assert decode['sub'] == str(user_id)
    assert decode['exp'] == int((expire_delta + datetime.now()).timestamp())

def test_decode():
    audience = "mobile_app"
    user_id = "1"
    token, _ = auth.create_access_token(user_id, timedelta(seconds=10), aud=audience)
    decode = auth.decode(token, audience)

    assert decode['aud'] == audience
    assert decode['sub'] == user_id

    
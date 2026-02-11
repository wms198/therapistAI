from pwdlib import PasswordHash
from pydantic import BaseModel
from therapistai.db.models import User

password_hash = PasswordHash.recommended()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import TEXT

class Message(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(sa_column=Column(TEXT))
    role: str
    create_at: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    user_id: int | None = Field(default=None, foreign_key="user.id")

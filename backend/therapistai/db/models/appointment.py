from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, TIMESTAMP


class Appointment(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    start_at: Optional[datetime] = Field(sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
        ))
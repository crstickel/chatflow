
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Column
from typing import Optional
import uuid

from shared.column import DateTimeUTC
from shared.time import get_current_time

class User(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: User.generate_id())
    username: str
    email: EmailStr
    pwhash: str
    created_at: datetime = Field(default_factory=get_current_time, sa_column=Column(DateTimeUTC))
    deleted_at: Optional[datetime] = None


    @classmethod
    def generate_id(cls) -> str:
        return str(uuid.uuid4())



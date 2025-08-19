
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from pydantic import EmailStr
import uuid

from shared.column import DateTimeUTC
from shared.time import get_current_time

class Conversation(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: Conversation.generate_id())
    name: str
    created_at: datetime = Field(default_factory=get_current_time, sa_column=Column(DateTimeUTC))

    @classmethod
    def generate_id(cls) -> str:
        return str(uuid.uuid4())


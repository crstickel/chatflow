
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from typing import Optional

from shared.column import DateTimeUTC
from shared.time import get_current_time

class Message(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    conversation_id: str
    sender_id: str
    content: str
    created_at: datetime = Field(default_factory=get_current_time, sa_column=Column(DateTimeUTC))


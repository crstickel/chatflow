
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from typing import Optional

from shared.column import DateTimeUTC
from shared.time import get_current_time

class Membership(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    conversation_id: str
    created_at: datetime = Field(default_factory=get_current_time, sa_column=Column(DateTimeUTC))


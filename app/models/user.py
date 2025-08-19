
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class User(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: User.generate_id())
    username: str
    email: EmailStr
    pwhash: str
    created_at: datetime
    deleted_at: Optional[datetime] = None


    @classmethod
    def generate_id(cls) -> str:
        return str(uuid.uuid4())



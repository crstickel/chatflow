
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    pwhash: str
    created_at: datetime
    deleted_at: Optional[datetime] = None


    @classmethod
    def generate_id(cls) -> str:
        return str(uuid.uuid4())



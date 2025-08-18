
from datetime import datetime
from pydantic import BaseModel, EmailStr
import uuid

class Conversation(BaseModel):
    id: str
    name: str
    created_at: datetime

    @classmethod
    def generate_id(cls) -> str:
        return str(uuid.uuid4())


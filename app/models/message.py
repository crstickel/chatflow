
from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int = Field
    conversation_id: str
    sender_id: str
    content: str
    created_at: datetime



from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from .conversation import Conversation

class Message(SQLModel, table=true):
    id: int = Field
    conversation_id: str
    sender_id: str
    content: str
    created_at: datetime


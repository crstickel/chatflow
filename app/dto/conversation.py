
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List

class PublicConversationDTO(BaseModel):
    name: str
    participants: List[str]


class NewConversationRequestDTO(BaseModel):
    name: str
    participants: list[str]


class SendMessageDTO(BaseModel):
    content: str


class ConversationMessageDTO(BaseModel):
    id: int
    created_at: datetime
    sender: str
    sender_id: str
    content: str

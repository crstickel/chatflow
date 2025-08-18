
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List

class PublicConversationDTO(BaseModel):
    name: str
    participants: List[str]


class NewConversationRequestDTO(BaseModel):
    name: str
    participants: list[str]


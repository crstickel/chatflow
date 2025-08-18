
from datetime import datetime
from pydantic import BaseModel

class Membership(BaseModel):
    user_id: str
    conversation_id: str


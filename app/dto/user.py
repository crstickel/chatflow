
from datetime import datetime
from pydantic import BaseModel, EmailStr

class PublicUserDTO(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime


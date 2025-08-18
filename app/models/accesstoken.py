
from datetime import datetime, timedelta
from pydantic import BaseModel
import secrets

from app.config import settings

class AccessToken(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    time_to_live: int


    @classmethod
    def generate_id(cls) -> str:
        return secrets.token_urlsafe(settings.OAUTH2_TOKEN_ENTROPY_BITS//8)


    @classmethod
    def default_time_to_live(cls) -> int:
        return settings.OAUTH2_ACCESS_TOKEN_TIME_TO_LIVE


    @property
    def expires_at(self):
        return self.created_at + timedelta(seconds=self.time_to_live)


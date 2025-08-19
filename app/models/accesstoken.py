
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Field, Column
import secrets

from app.config import settings
from shared.column import DateTimeUTC
from shared.time import get_current_time

class AccessToken(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: AccessToken.generate_id())
    user_id: str
    created_at: datetime = Field(default_factory=get_current_time, sa_column=Column(DateTimeUTC))
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


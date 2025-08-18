
from pydantic import BaseModel

class RegisterRequestDTO(BaseModel):
    email: str
    username: str
    password: str


class LoginResponseDTO(BaseModel):
    access_token: str
    token_type: str
    expires_in: int | None
    scope: str


import datetime
from pydantic import BaseModel , EmailStr , SecretStr


class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr


class UserRegisterResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime.datetime
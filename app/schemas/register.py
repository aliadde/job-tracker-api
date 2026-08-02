import datetime
from pydantic import BaseModel , EmailStr , SecretStr, Field


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(min_length=5, max_length=100)
    password: SecretStr = Field(min_length=8, max_length=20)


class UserRegisterResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime.datetime
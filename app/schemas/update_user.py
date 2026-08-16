import pydantic

class UpdateUserRequest(pydantic.BaseModel):
    username: str | None = None
    email: pydantic.EmailStr | None = None
    password: str | None = None

from pydantic import BaseModel

class CreateCompanyRequest(BaseModel):
    name: str
    location : str | None = None

class CreateCompanyResponse(BaseModel):
    id: int
    name: str
    location: str | None


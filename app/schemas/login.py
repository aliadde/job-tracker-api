from pydantic import BaseModel

class UserLoginRequest(BaseModel):
    username: str
    password: str
    
    
class UserLoginResponse(BaseModel):
    jwt : str
    
class JWTPayload(BaseModel):
    id: int
    username: str
from pydantic import BaseModel

class UserLoginRequest(BaseModel):
    username: str
    password: str
    
    
class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str
    
class JWTPayload(BaseModel):
    id: int
    username: str
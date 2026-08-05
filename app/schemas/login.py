from pydantic import BaseModel

class UserLoginRequest(BaseModel):
    username: str
    password: str
    
    
class UserLoginResponse(BaseModel):
    jwt : str
    refresh_token : str
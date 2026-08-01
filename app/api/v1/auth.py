from app.main import router
from app.db.database import get_db
from fastapi import  Depends 
from sqlalchemy.orm import Session

from app.schemas.register import UserRegisterRequest, UserRegisterResponse
from app.services.auth_services import AuthService

# ========== Dependencies ==========
def get_auth_service() -> AuthService:
    return AuthService()
# ==================================

@router.post("/register", response_model=UserRegisterResponse)
async def register(
        user_data:UserRegisterRequest ,
        auth_service: AuthService = Depends(get_auth_service),
        db: Session = Depends(get_db)
    ):

    return await auth_service.register(db, user_data)
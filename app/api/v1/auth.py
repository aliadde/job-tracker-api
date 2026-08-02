from app.main import router
from app.db.database import get_db
from fastapi import  Depends ,status
from sqlalchemy.orm import Session

from app.repositories.auth import AuthRepository
from app.schemas.register import UserRegisterRequest, UserRegisterResponse
from app.services.auth_services import AuthService

# ========== Dependencies ==========
def get_auth_service() -> AuthService:
    return AuthService()


def get_auth_repository() -> AuthRepository:
    return AuthRepository()
# ==================================

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRegisterResponse)
async def register(
        user_data:UserRegisterRequest ,
        auth_service: AuthService = Depends(get_auth_service),
        db: Session = Depends(get_db),
        user_crud = Depends(get_auth_repository)
    ):
    
    return await auth_service.register(db, user_data,  user_crud)
from fastapi.security import OAuth2PasswordBearer

from app.db.database import get_db
from fastapi import  Depends ,status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.app import AppRepository
from app.repositories.auth import AuthRepository
from app.services.app import AppService
from app.services.auth import AuthService
from app.schemas.app import CreateAppRequest
# ========== Dependencies ==========
def get_app_service() -> AppService:
    return AppService()

def get_auth_service() -> AuthService:
    return AuthService()

def get_user_repository() -> AuthRepository:
    return AuthRepository()

def get_app_repository() -> AppRepository:
    return AppRepository()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# ==================================
# creating router
router = APIRouter()
# ==================================
@router.post("/app", status_code=status.HTTP_200_OK)
async def current_user(
        new_app_data: CreateAppRequest ,
        token: str =  Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        app_service: AppService = Depends(get_app_service),
        auth_service: AuthService = Depends(get_auth_service),
        user_crud: AuthRepository = Depends(get_user_repository),
        app_crud: AppRepository = Depends(get_app_repository)
    ):
    # first check the token sends from user is valid or not
    user = await auth_service.validate_token(
        token = token,
        db = db,
        user_crud = user_crud
    )
    
    # the validations was successfull so we can add app for user
    app_service.create(db, app_crud, new_app_data, user)
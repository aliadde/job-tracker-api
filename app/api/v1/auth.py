from fastapi.security import OAuth2PasswordBearer

from app.db.database import get_db
from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.auth import AuthRepository
import app.schemas.register as schema_register
import app.schemas.login as schema_login
from app.services.auth import AuthService


# ========== Dependencies ==========
def get_auth_service() -> AuthService:
    return AuthService()


def get_auth_repository() -> AuthRepository:
    return AuthRepository()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# ==================================
# creating router
router = APIRouter()
# ==================================


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schema_register.UserRegisterResponse,
)
async def register(
    user_data: schema_register.UserRegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
    user_crud=Depends(get_auth_repository),
):
    return await auth_service.register(db, user_data, user_crud)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=schema_login.UserLoginResponse,
)
async def login(
    user_data: schema_login.UserLoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
    user_crud=Depends(get_auth_repository),
):
    return await auth_service.login(db, user_data, user_crud)


@router.get(
    "/current_user",
    status_code=status.HTTP_200_OK
)
async def current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
    user_crud=Depends(get_auth_repository),
):
    user = await auth_service.validate_token(token=token, db=db,user_crud=user_crud)

    return await auth_service.get_current_user(user, db, user_crud)

@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service),
    db: AsyncSession = Depends(get_db),
    user_crud=Depends(get_auth_repository),
):
    user = await auth_service.validate_token(
        token=token,
        db=db,
        user_crud=user_crud,
    )

    return await auth_service.delete(
        user=user,
        db=db,
        user_crud=user_crud,
    )
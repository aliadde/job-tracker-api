from fastapi.security import OAuth2PasswordBearer
import typing
from app.db.database import get_db
from fastapi import Depends, status, APIRouter, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.auth import AuthRepository
import app.schemas.register as schema_register
import app.schemas.login as schema_login
from app.services.auth import AuthService
from app.schemas.update_user import UpdateUserRequest


# ========== Dependencies ==========
def get_auth_service() -> AuthService:
    return AuthService()


def get_auth_repository() -> AuthRepository:
    return AuthRepository()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# ==================================
# creating router
router = APIRouter()

# ============================================= REEGISTER / SIGN UP ===============================
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

# ============================================= LOGIN /SIGN IN ===============================
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

# ============================================= GET CURRENT USER ===============================
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

# ============================================= DELETE ===============================
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
    
# ============================================= UPDATE ===============================
@router.patch("/update", status_code=status.HTTP_200_OK)
async def update_user(
    update_data: UpdateUserRequest ,
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

    # remove not filled field from update data
    update_data: dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
    return await auth_service.update(
        db=db,
        user=user,
        update_data=update_data,
        user_crud=user_crud,
    )


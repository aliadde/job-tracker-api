from fastapi.security import OAuth2PasswordBearer

from app.db.database import get_db
from fastapi import  Depends ,status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.app import AppRepository
from app.repositories.auth import AuthRepository
from app.services.app import AppService
from app.services.auth import AuthService
from app.schemas.app import (
    CreateAppRequest, CreateAppResponse,
     DeleteAppResponse,
     UpdateAppRequest, UpdateAppResponse,
     GetAllAppResponse
)
from app.models import Users

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

# ================================== create app ====================================================================
@router.post("/app", status_code=status.HTTP_201_CREATED, response_model=CreateAppResponse)
async def create_app(
        new_app_data: CreateAppRequest ,
        token: str =  Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        app_service: AppService = Depends(get_app_service),
        auth_service: AuthService = Depends(get_auth_service),
        user_crud: AuthRepository = Depends(get_user_repository),
        app_crud: AppRepository = Depends(get_app_repository)
    ):
    # first check the token sends from user is valid or not
    user: Users = await auth_service.validate_token(
        token = token,
        db = db,
        user_crud = user_crud
    )
    
    # the validations was successfull so we can add app for user
    # NOTE: dict(new_app_data): this is used to convert the CreateAppRequest object (pydantic object) into a dictionary
    return await app_service.create(
        db,
        app_crud, 
        dict(new_app_data),
        user
    )
    
# ================================== delete app ====================================================================
@router.delete("/app/id/{app_id}", status_code=status.HTTP_200_OK, response_model=DeleteAppResponse)
async def delete_app_by_id(
        app_id: int,
        token: str =  Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        app_service: AppService = Depends(get_app_service),
        auth_service: AuthService = Depends(get_auth_service),
        user_crud: AuthRepository = Depends(get_user_repository),
        app_crud: AppRepository = Depends(get_app_repository)
    ):
    # first check the token sends from user is valid or not
    user: Users = await auth_service.validate_token(
        token = token,
        db = db,
        user_crud = user_crud
    )
    
    # the validations was successfull so we can delete app for user
    return await app_service.delete(
        db,
        app_crud, 
        app_id,
        user
    )

@router.delete("/app/title/{app_title}", status_code=status.HTTP_200_OK, response_model=DeleteAppResponse)
async def delete_app_by_title(
        app_title: str,
        token: str =  Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        app_service: AppService = Depends(get_app_service),
        auth_service: AuthService = Depends(get_auth_service),
        user_crud: AuthRepository = Depends(get_user_repository),
        app_crud: AppRepository = Depends(get_app_repository)
    ):
    # first check the token sends from user is valid or not
    user: Users = await auth_service.validate_token(
        token = token,
        db = db,
        user_crud = user_crud
    )
    
    # the validations was successfull so we can delete app for user
    return await app_service.delete(
        db,
        app_crud, 
        app_title,
        user
    )
    
# ================================== update app ====================================================================
@router.patch("/app/update/title/{app_title}", status_code=status.HTTP_200_OK, response_model=UpdateAppResponse)
async def update_app_by_title(
        app_title: str,
        data: UpdateAppRequest,
        token: str =  Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        app_service: AppService = Depends(get_app_service),
        auth_service: AuthService = Depends(get_auth_service),
        user_crud: AuthRepository = Depends(get_user_repository),
        app_crud: AppRepository = Depends(get_app_repository)
    ):
    # first check the token sends from user is valid or not
    user: Users = await auth_service.validate_token(
        token = token,
        db = db,
        user_crud = user_crud
    )
    
    # the validations was successfull so we can update app for user
    # NOTE: dict(updated_data): this is used to convert the CreateAppRequest object (pydantic object) into a dictionary
    
    # remove field from model  NOT send from user
    updated_data = data.model_dump(exclude_unset=True)

    return await app_service.update(
        db,
        app_crud,
        app_title,
        dict(updated_data),
        user
    )

@router.patch("/app/update/id/{app_id}", status_code=status.HTTP_200_OK, response_model=UpdateAppResponse)
async def update_app_by_id(
        app_id: int,
        data: UpdateAppRequest,
        token: str =  Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        app_service: AppService = Depends(get_app_service),
        auth_service: AuthService = Depends(get_auth_service),
        user_crud: AuthRepository = Depends(get_user_repository),
        app_crud: AppRepository = Depends(get_app_repository)
    ):
    # first check the token sends from user is valid or not
    user: Users = await auth_service.validate_token(
        token = token,
        db = db,
        user_crud = user_crud
    )
    
    # the validations was successfull so we can update app for user
    # NOTE: dict(updated_data): this is used to convert the CreateAppRequest object (pydantic object) into a dictionary
    
    # remove field from model  NOT send from user
    updated_data = data.model_dump(exclude_unset=True)

    return await app_service.update(
        db,
        app_crud,
        app_id,
        dict(updated_data),
        user
    )

# ================================== read app ====================================================================
@router.get("/app/all", status_code=status.HTTP_200_OK,)
async def get_all_app(
        token: str =  Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db),
        app_service: AppService = Depends(get_app_service),
        auth_service: AuthService = Depends(get_auth_service),
        user_crud: AuthRepository = Depends(get_user_repository),
        app_crud: AppRepository = Depends(get_app_repository),
    ):
    # first check the token sends from user is valid or not
    user: Users = await auth_service.validate_token(
        token = token,
        db = db,
        user_crud = user_crud
    )


    # the validations was successfull so we can give apps to user
    return await app_service.get_all(
        db,
        app_crud,
        user,
    )

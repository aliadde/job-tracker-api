import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from app.schemas.register import UserRegisterRequest
from fastapi import HTTPException


# ========= Login ============================
@pytest.fixture
def login_setup():
    db = Mock()
    repository = AsyncMock()
    token: str= "1.2.3" 
    user_data_rq: dict = Mock()
    return db, repository, token, user_data_rq

@pytest.mark.asyncio
async def test_login_success(login_setup):
    from app.models.users import Users
    db, repository, token, user_data_rq = login_setup
    
    user =  Users(
        id=0,
        username="testuser",
        hashed_password = "passwordtest",
        is_active = True
    )
    
    repository.get_by_username.return_value = user
    
    user_data_rq.username = "testuser"
    user_data_rq.password = "passwordtest"

    services: AuthService = AuthService()
    
    with patch("app.services.auth.verify_password") as patched_verify_password:
        with patch("app.services.auth.create_jwt_token") as patched_create_jwt_token:
            # password hashed ckeck mocking ✅
            patched_verify_password.return_value = True
            # after this fase the system must create jwt token
            patched_create_jwt_token.return_value = token
            result = await services.login(
                        db=db,
                        data=user_data_rq,
                        user_crud=repository
                    )

            patched_verify_password.assert_not_called
            patched_create_jwt_token.assert_called_once
    
    repository.get_by_username.assert_awaited_once_with(
        db=db,
        username=user_data_rq.username
    )
        
    assert result.get("access_token") == token
    assert result.get("token_type") == "bearer"
    
        
    
@pytest.mark.asyncio
async def test_login_fail_username_incorrect(login_setup):
    db, repository, token, user_data_rq = login_setup
    
    repository.get_by_username.return_value = None

    user_data_rq.username = "testuser"
    user_data_rq.password = "passwordtest"
    
    services: AuthService = AuthService()
    
    with patch("app.services.auth.verify_password") as patched_verify_password:
        with patch("app.services.auth.create_jwt_token") as patched_create_jwt_token:
            with pytest.raises(HTTPException) as exc_info:

                result = await services.login(
                            db=db,
                            data=user_data_rq,
                            user_crud=repository
                )
                # Assert
                assert exc_info.value.status_code == 404
                assert exc_info.value.detail == "invalid username or password"
                patched_verify_password.assert_not_called
                patched_create_jwt_token.assert_not_called
                repository.get_by_username.assert_awaited_once_with(
                        db=db,
                        username=user_data_rq.username
                    )

        

@pytest.mark.asyncio
async def test_login_fail_password_incorreect(login_setup):
    from app.models.users import Users
    db, repository, token, user_data_rq = login_setup
    
    user =  Users(
        id=0,
        username="testuser",
        hashed_password = "passwordtest"
    )
    repository.get_by_username.return_value = user

    user_data_rq.username = "testuser"
    user_data_rq.password = "paswordte"
    
    services: AuthService = AuthService()
    
    with patch("app.services.auth.verify_password") as patched_verify_password:
        with patch("app.services.auth.create_jwt_token") as patched_create_jwt_token:
            # password hashed ckeck mocking ✅
            patched_verify_password.return_value = False
            # after this fase the system must create jwt token
            with pytest.raises(HTTPException) as exc_info:
                result = await services.login(
                            db=db,
                            data=user_data_rq,
                            user_crud=repository
                        )
                assert exc_info.value.status_code == 404
                assert exc_info.value.detail == "invalid username or password"
                

            patched_verify_password.assert_not_called
            patched_create_jwt_token.assert_not_called
    
    repository.get_by_username.assert_awaited_once_with(
        db=db,
        username=user_data_rq.username
    )
        
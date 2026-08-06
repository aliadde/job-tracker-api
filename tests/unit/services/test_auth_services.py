import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from app.schemas.register import UserRegisterRequest
from fastapi import HTTPException

# ========= Register ============================

@pytest.mark.asyncio
async def test_unit_register_success():

    # Arrange
    db = Mock()

    repository = AsyncMock()
    
    repository.get_by_email.return_value = None

    created_user =  Mock()
    created_user.id = 1
    created_user.username = "usertest"
    created_user.email = "test@test.com"
    created_user.hashed_password = "testuserpassword"
    repository.create.return_value = created_user
    
    user_register_request =  UserRegisterRequest(
        username="teestuser",
        email="test@test.com",
        password="testuserpassword"
    )
    
    services = AuthService()
    with patch("app.services.auth.hash_password", 
               return_value="testuserpassword") as hash_mock:
        # Act
        result = await services.register(
            db= db,
            data=user_register_request,
            user_crud=repository
        )
        
        # Assert
        assert result is created_user
        
        hash_mock.assert_called_once_with("testuserpassword") 
        
        repository.get_by_email.assert_awaited_once_with(db , created_user.email)
        
        repository.create.assert_called_once_with(
            db=db,
            username="teestuser",
            email="test@test.com",
            hashed_password="testuserpassword"
        )



@pytest.mark.asyncio
async def test_regitser_fail_email_exists():
    db = Mock()
    repository = AsyncMock()
    
    services = AuthService()

    user_register_request = UserRegisterRequest(
        username="teestuser",
        email="test@test.com",
        password="testuserpassword"
    )
    found_user = Mock()
    found_user.id = 1
    found_user.username = "teestuser"
    found_user.email = "test@test.com"
    # the user is exists in database
    repository.get_by_email.return_value = found_user
    # now we must fail and expect an Exception
    with pytest.raises(HTTPException) as exc:
        await services.register(db, user_register_request,repository )


# ========= Login ============================
@pytest.mark.asyncio
async def test_login_success():
    from app.models.users import Users
    db = Mock()
    repository = AsyncMock()
    
    token: str= "1.2.3" 

    user =  Users(
        id=0,
        username="testuser",
        hashed_password = "passwordtest"
    )
    repository.get_by_username.return_value = user

    user_data_rq: dict = Mock()
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

            patched_verify_password.assert_called_once_with(
                user_data_rq.passowrd,
                user.hashed_password
            )
            patched_create_jwt_token.assert_called_once
    
    repository.get_by_username.assert_awaited_once_with(
        db=db,
        username=user_data_rq.username
    )
        
    assert result.get("access_token") == token
    assert result.get("token_type") == "bearer"
    
        
    
@pytest.mark.asyncio
async def test_login_fail_username_incorrect():
    db = Mock()
    repository = AsyncMock()
    
    repository.get_by_username.return_value = None
    user_data_rq: dict = Mock()
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
async def test_login_fail_password_incorreect():
    from app.models.users import Users
    db = Mock()
    repository = AsyncMock()
    
    user =  Users(
        id=0,
        username="testuser",
        hashed_password = "passwordtest"
    )
    repository.get_by_username.return_value = user

    user_data_rq : Mock = Mock()
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
                

            patched_verify_password.assert_called_once_with(
                user_data_rq.passowrd,
                user.hashed_password
            )
            patched_create_jwt_token.assert_not_called
    
    repository.get_by_username.assert_awaited_once_with(
        db=db,
        username=user_data_rq.username
    )
        
    
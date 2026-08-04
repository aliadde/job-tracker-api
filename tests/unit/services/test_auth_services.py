import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from app.schemas.register import UserRegisterRequest
from fastapi import HTTPException


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
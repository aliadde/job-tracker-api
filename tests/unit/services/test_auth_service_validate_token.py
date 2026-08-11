import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from app.schemas.register import UserRegisterRequest
from fastapi import HTTPException

# ===============
# validate token moethod

@pytest.fixture
def setup_validate_token():

    class TestApplication:
        title = "Test Application"
    
    db = AsyncMock()
    repository = AsyncMock()
    
    service = AuthService()
    expected_found_user = Mock()
    expected_found_user.id = 0
    expected_found_user.username = "testuser"
    expected_found_user.email = "testuser@example.com"
    expected_found_user.is_active = True
    expected_found_user.created_at = "2026-08-06 12:18:12.891620"
    expected_found_user.update_at= "2026-08-07 12:18:12.891620"
    expected_found_user.applications = [TestApplication()]

    return db ,repository, service, expected_found_user

@pytest.mark.asyncio
@patch("app.services.auth.decode_jwt_token")
async def test_validate_user(mocked_decode_jwt_token, setup_validate_token):
    
    db, repository, service, expected_found_user = setup_validate_token
    
    expected_payload : dict ={
        "id": 0,
        "username": "testuser",
        "active": True
    }
    
    mocked_decode_jwt_token.return_value = expected_payload

    repository.get_by_username.return_value = expected_found_user
    
    current_user_response  = await service.validate_token(
        token="1.2.3",
        db=db,
        user_crud=repository
    )

    # Asserts 
    mocked_decode_jwt_token.assert_called_once
    repository.get_by_username.assert_called_once_with(db=db, username="testuser")
    assert current_user_response.username == expected_found_user.username
    assert current_user_response.is_active == expected_found_user.is_active
    assert current_user_response.created_at == expected_found_user.created_at
    assert current_user_response.update_at == expected_found_user.update_at
    assert len(current_user_response.applications) == 1
    

@pytest.mark.asyncio
@patch("app.services.auth.decode_jwt_token")
async def test_validate_user_jwt_token_error(mocked_decode_jwt_token, setup_validate_token):
    db, repository, service, expected_found_user = setup_validate_token
    
    mocked_decode_jwt_token.return_value = None
    with pytest.raises(HTTPException) as exc:
        await service.validate_token(
            token="1.2.3",
            db=db,
            user_crud=repository
        )
    assert exc.value.status_code == 401
    assert exc.value.detail == "Not authenticated"
    

@pytest.mark.asyncio
@patch("app.services.auth.decode_jwt_token")
async def test_validate_user_get_by_username_error(mocked_decode_jwt_token, setup_validate_token):
    db, repository, service, expected_found_user = setup_validate_token
    
    expected_payload : dict ={
        "id": 0,
        "username": "testuser",
        "active": True
    }
    mocked_decode_jwt_token.return_value = expected_payload
    
    # database return None
    repository.get_by_username.return_value = None
    
    with pytest.raises(HTTPException) as exc:
        await service.validate_token(
            token="1.2.3",
            db=db,
            user_crud=repository
        )
        
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"
import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from app.schemas.register import UserRegisterRequest
from fastapi import HTTPException


# ============================ current_user ============================
@pytest.fixture
def get_current_user():
    class TestCompany:
        name = "Test Company"

    class TestApplication:
        title = "Test Application"

    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
    
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
    expected_found_user.companies = [TestCompany()]
    expected_found_user.applications = [TestApplication()]

    return db ,repository, service, expected_found_user, Struct
    
@pytest.mark.asyncio
@patch("app.services.auth.decode_jwt_token")
async def test_get_current_user_successfully(mocked_decode_jwt_token, get_current_user):

    db, repository, service, expected_found_user, Struct = get_current_user
    
    expected_payload : dict ={
        "id": 0,
        "username": "testuser",
        "active": True
    }
    
    mocked_decode_jwt_token.return_value = expected_payload

    repository.get_by_username.return_value = expected_found_user
    
    current_user_response  = await service.get_current_user(
        token="1.2.3",
        db=db,
        user_crud=repository
    )

    # Asserts 
    current_user_response = Struct(**current_user_response)
    mocked_decode_jwt_token.assert_called_once
    repository.get_by_username.assert_called_once_with(db=db, username="testuser")
    assert current_user_response.username == expected_found_user.username
    assert current_user_response.is_active == expected_found_user.is_active
    assert current_user_response.created_at == expected_found_user.created_at
    assert current_user_response.update_at == expected_found_user.update_at
    assert len(current_user_response.applications) == 1
    
@pytest.mark.asyncio
@patch("app.services.auth.decode_jwt_token")
async def test_current_user_deactive(mocked_decode_jwt_token, get_current_user):
    db, repository, service, expected_found_user, Struct= get_current_user
    
    expected_payload : dict ={
        "id": 0,
        "username": "testuser",
        "active": False
    }
    
    mocked_decode_jwt_token.return_value = expected_payload

    expected_found_user.active = False

    repository.get_by_username.return_value = expected_found_user
    with pytest.raises(HTTPException) as ext:
        
        current_user_response  = await service.get_current_user(
            token="1.2.3",
            db=db,
            user_crud=repository
        )
        
    assert ext.type == HTTPException
    assert ext.value.status_code == 400
    assert ext.value.detail == "Inactive user"
    mocked_decode_jwt_token.assert_called_once
    repository.get_by_username.assert_not_called()
    

@pytest.mark.asyncio
@patch("app.services.auth.decode_jwt_token")
async def test_current_user_not_found(mocked_decode_jwt_token, get_current_user):
    db, repository, service, expected_found_user, Struct= get_current_user
    
    expected_payload : dict ={
        "id": 0,
        "username": "estuser",
        "active": True
    }
    
    mocked_decode_jwt_token.return_value = expected_payload

    repository.get_by_username.return_value = None
    with pytest.raises(HTTPException) as ext:
        
        current_user_response  = await service.get_current_user(
            token="1.2.3",
            db=db,
            user_crud=repository
        )
        
    assert ext.type == HTTPException
    assert ext.value.status_code == 404
    assert ext.value.detail == "User not found"
    mocked_decode_jwt_token.assert_called_once
    repository.get_by_username.assert_called_once_with(db=db,username=expected_payload["username"])
    

@pytest.mark.asyncio
@patch("app.services.auth.decode_jwt_token")
async def test_get_current_user_invalid_token(mocked_decode_jwt_token, get_current_user):
    db, repository, service, expected_found_user, Struct= get_current_user
    
    expected_payload : dict ={
        "id": 0,
        "username": "testuser",
        "active": True
    }
    
    mocked_decode_jwt_token.return_value = None

    with pytest.raises(HTTPException) as ext:
        
        current_user_response  = await service.get_current_user(
            token="1.2.3",
            db=db,
            user_crud=repository
        )
        
    assert ext.type == HTTPException
    assert ext.value.status_code == 401
    assert ext.value.detail == "Not authenticated"
    mocked_decode_jwt_token.assert_called_once
    repository.get_by_username.assert_not_called()
    

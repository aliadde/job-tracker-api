import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from fastapi import HTTPException
from app.models.users import Users

# ============================ current_user ============================
@pytest.fixture
def get_current_user():

    class TestApplication:
        title = "Test Application"

    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
    
    db = AsyncMock()
    repository = AsyncMock()
    
    service = AuthService()
    expected_found_user = Mock()
    expected_found_user.id = 1
    expected_found_user.username = "testuser"
    expected_found_user.email = "testuser@example.com"
    expected_found_user.is_active = True
    expected_found_user.created_at = "2026-08-06 12:18:12.891620"
    expected_found_user.update_at= "2026-08-07 12:18:12.891620"
    expected_found_user.applications = [TestApplication()]

    return db ,repository, service, expected_found_user, Struct
    
@pytest.mark.asyncio
async def test_get_current_user_successfully(get_current_user):

    db, repository, service, expected_found_user, Struct = get_current_user
    
    

    current_user_response : dict = await service.get_current_user(
        user=expected_found_user,
        db=db,
        user_crud=repository
    )

    # Asserts 
    assert current_user_response.get("username") == expected_found_user.username
    assert current_user_response.get("is_active") == expected_found_user.is_active
    assert current_user_response.get("created_at") == expected_found_user.created_at
    assert current_user_response.get("update_at") == expected_found_user.update_at
    assert len(current_user_response.get("applications")) == 1

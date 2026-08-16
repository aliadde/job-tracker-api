import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from app.schemas.register import UserRegisterRequest
from fastapi import HTTPException


# ============================  ============================
@pytest.fixture
def setup():

    db = AsyncMock()
    repository = AsyncMock()
    
    service = AuthService()
    
    return db ,repository, service

@pytest.mark.anyio
async def test_delete_user(setup):
    """
    Delete a user from database.
    """
    mocked_db, mocked_repository, auth_service = setup
    
    mocked_user = Mock()
    mocked_repository.get_by_id.return_value = mocked_user
    
    mocked_repository.delete.return_value = mocked_user
    result = await auth_service.delete(
        user_id=1,
        db=mocked_db,
        user_crud=mocked_repository,
    )
    assert result == mocked_user

@pytest.mark.anyio
async def test_delete_user_fail_not_found_user(setup):
    """
    Delete a user but not found user.
    """
    mocked_db, mocked_repository, auth_service = setup

    mocked_user = Mock()
    mocked_repository.get_by_id.return_value = None

    mocked_repository.delete.return_value = mocked_user
    with pytest.raises(HTTPException) as ex:
        await auth_service.delete(
            user_id=1,
            db=mocked_db,
            user_crud=mocked_repository,
        )

    assert ex.value.status_code == 404
    assert ex.value.detail == "User not found"

import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.auth import AuthService
from app.schemas.register import UserRegisterRequest
from fastapi import HTTPException
from app.models.users import Users

# ============================  ============================
@pytest.fixture
def setup():

    db = AsyncMock()
    repository = AsyncMock()
    
    service = AuthService()
    
    mocked_user = Users(id=1)
    mocked_user.hashed_password = "aflkasfjsfjs;f"
    mocked_user._sa_instance_state = "asdf"
    return db ,repository, service,mocked_user

@pytest.mark.anyio
async def test_delete_user(setup):
    """
    Delete a user from database.
    """
    mocked_db, mocked_repository,\
        auth_service, mocked_user = setup


    mocked_repository.delete.return_value = mocked_user
    result = await auth_service.delete(
        user=mocked_user,
        db=mocked_db,
        user_crud=mocked_repository,
    )
    assert result.get("id") == mocked_user.id

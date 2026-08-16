from unittest.mock import Mock,AsyncMock, patch
import pytest
from app.services.auth import AuthService
from app.models.users import Users
# =================== fixture ====================
@pytest.fixture
def create_mock():
    db= AsyncMock()
    user_crud = AsyncMock()
    user = Mock()
    auth_service = AuthService()
    return db, user_crud, user, auth_service


# =================== test =======================
@pytest.mark.anyio
@patch('app.services.auth.security.hash_password')
async def test_update_user_success(patched_hash_password, create_mock):
    mocked_db, mocked_user_crud, mocked_user, auth_service = create_mock
    update_data = dict(
        username="new username",
        email="new_email",
        password="new_password",
    )

    patched_hash_password.return_value = '1.2.3'
    mock_updated_user = Mock()
    mock_updated_user.id=1
    mock_updated_user.username=update_data.get("username")
    mock_updated_user.email=update_data.get("email")
    mock_updated_user.hashed_password="1.2.3"
    mocked_user_crud.update_user.return_value = mock_updated_user
    
    
    result = await auth_service.update(
        db=mocked_db,
        user= mocked_user,
        update_data= update_data,
        user_crud=mocked_user_crud,
    )


    assert not hasattr(result, "hashed_password")
    mocked_user_crud.update_user.assert_awaited_once
    patched_hash_password.assert_called_once_with("new_password")
    

@pytest.mark.anyio
@patch('app.services.auth.security.hash_password')
async def test_update_user_with_no_password_change(patched_hash_password, create_mock):
    mocked_db, mocked_user_crud, mocked_user, auth_service = create_mock
    update_data = dict(
        username="new username",
        email="new_email",
    )

    
    mock_updated_user = Mock()
    mock_updated_user.id=1
    mock_updated_user.username=update_data.get("username")
    mock_updated_user.email=update_data.get("email")
    mock_updated_user.hashed_password="1.2.3"
    mocked_user_crud.update_user.return_value = mock_updated_user
    
    result = await auth_service.update(
        db=mocked_db,
        user= mocked_user,
        update_data= update_data,
        user_crud=mocked_user_crud,
    )
    assert not hasattr(result, "hashed_password")
    assert  hasattr(result, "username")
    assert  hasattr(result, "email")
    assert  hasattr(result, "id")
    mocked_user_crud.update_user.assert_awaited_once
    patched_hash_password.assert_not_called
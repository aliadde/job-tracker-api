import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.app import AppService
from app.schemas.app import DeleteAppRequest
from fastapi import HTTPException
# ================= setup =================
@pytest.fixture
def setup():
    mocked_db = AsyncMock()
    mocked_repository = AsyncMock()
    return mocked_db, mocked_repository
    # "position": "Full-time",
    # "job": "Software Engineer"

@pytest.fixture
def app_service():
    return AppService()

# ================ test =================
@pytest.mark.anyio
async def test_app_service_delete_app_success(setup, app_service: AppService):
    """ Test app service delete app success  """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mocking method repository 
    # found app mocked
    mocked_found_app = Mock()
    mocked_found_app.id = 1
    mocked_found_app.title = None
    mocked_found_app.user_id = 1
    mocked_repository.get_app_by_id.return_value = mocked_found_app

    # mocking repository delete method
    mocked_repository.delete.return_value =  mocked_found_app
    
    # mocked user
    mocked_user = Mock()
    mocked_user.id = 1
    # request data
    app_data = {
        "id": 1
    }
    
    deleted_app = await app_service.delete(
        db= mocked_db,
        app_crud=  mocked_repository,
        app_data= app_data,
        user=  mocked_user
    ) 
    assert deleted_app is not None
    assert deleted_app is mocked_found_app
    mocked_repository.get_app_by_id.assert_awaited_once
    mocked_repository.get_app_by_title.assert_not_awaited
    mocked_repository.delete.assert_awaited_once
    
@pytest.mark.anyio
async def test_app_service_delete_app_fail_not_found_app_with_id(setup, app_service: AppService):
    """ Test app service delete app fail not found app with id only """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mocking method repository 
    # found app mocked
    mocked_found_app = Mock()
    mocked_found_app.id = 1
    mocked_found_app.title = "test app"
    mocked_found_app.user_id = 1
    mocked_repository.get_app_by_id.return_value = None # will fail in this level
    

    # mocking repository delete method
    mocked_repository.delete.return_value =  mocked_found_app
    
    # mocked user
    mocked_user = Mock()
    mocked_user.id = 1
    # request data
    app_data = dict(
        id=1
    )
    with pytest.raises(HTTPException) as exc: 
        await app_service.delete(
            db= mocked_db,
            app_crud=  mocked_repository,
            app_data= app_data,
            user=  mocked_user
        ) 
    assert exc.value.status_code == 404
    assert exc.value.detail == "Application not found" 
    mocked_repository.get_app_by_id.assert_awaited_once
    mocked_repository.get_app_by_title.assert_not_awaited
    mocked_repository.delete.assert_not_awaited
    
@pytest.mark.anyio
async def test_app_service_delete_app_fail_not_found_app_with_title(setup, app_service: AppService):
    """ Test app service delete app fail not found app with title only  """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mocking method repository 
    # found app mocked
    mocked_found_app = Mock()
    mocked_found_app.title = "test app"
    mocked_found_app.user_id = 1
    mocked_repository.get_app_by_title.return_value = None # will fail in this level
    

    # mocking repository delete method
    mocked_repository.delete.return_value =  mocked_found_app
    
    # mocked user
    mocked_user = Mock()
    mocked_user.id = 1
    # request data
    app_data = dict(
        title="test app"
    )
    with pytest.raises(HTTPException) as exc: 
        await app_service.delete(
            db= mocked_db,
            app_crud=  mocked_repository,
            app_data= app_data,
            user=  mocked_user
        ) 
    assert exc.value.status_code == 404
    assert exc.value.detail == "Application not found" 
    mocked_repository.get_app_by_title.assert_awaited_once
    mocked_repository.get_app_by_id.assert_not_awaited
    mocked_repository.delete.assert_not_awaited
    
@pytest.mark.anyio
async def test_app_service_delete_app_fail_not_found_app_with_both_id_title(setup, app_service: AppService):
    """ Test app service delete app fail not found app with title and id provided. but 
    the logic will only check for title and not for id. 
    """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mocking method repository 
    # found app mocked
    mocked_found_app = Mock()
    mocked_found_app.title = "test app"
    mocked_found_app.user_id = 1
    mocked_repository.get_app_by_title.return_value = None # will fail in this level
    

    # mocking repository delete method
    mocked_repository.delete.return_value =  mocked_found_app
    
    # mocked user
    mocked_user = Mock()
    mocked_user.id = 1
    
    # request data
    app_data = dict(
        id=1,
        title="test app"
    )
    with pytest.raises(HTTPException) as exc: 
        await app_service.delete(
            db= mocked_db,
            app_crud=  mocked_repository,
            app_data= app_data,
            user=  mocked_user
        ) 
    assert exc.value.status_code == 404
    assert exc.value.detail == "Application not found" 
    mocked_repository.get_app_by_title.assert_awaited_once
    mocked_repository.get_app_by_id.assert_not_awaited
    mocked_repository.delete.assert_not_awaited
    
@pytest.mark.anyio
async def test_app_service_delete_app_fail_user_not_access(setup, app_service: AppService):
    """ 
    Test app service delete app fail because user not haae access to this application
    """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mocking method repository 
    # found app mocked
    mocked_found_app = Mock()
    mocked_found_app.title = "test app"
    mocked_found_app.user_id = 3
    mocked_repository.get_app_by_title.return_value = mocked_found_app # will fail in this level
    

    # mocking repository delete method
    mocked_repository.delete.return_value =  mocked_found_app
    
    # mocked user
    mocked_user = Mock()
    mocked_user.id = 1
    
    # request data
    app_data = dict(
        id=1,
        title="test app"
    )
    with pytest.raises(HTTPException) as exc: 
        await app_service.delete(
            db= mocked_db,
            app_crud=  mocked_repository,
            app_data= app_data,
            user=  mocked_user
        ) 
    assert exc.value.status_code == 401
    assert exc.value.detail == "You do not have access to this application" 
    mocked_repository.get_app_by_title.assert_awaited_once
    mocked_repository.get_app_by_id.assert_not_awaited
    mocked_repository.delete.assert_not_awaited


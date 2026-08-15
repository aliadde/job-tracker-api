import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.app import AppService
from fastapi import HTTPException
# ================= setup =================
@pytest.fixture
def setup():
    mocked_db = AsyncMock()
    mocked_repository = AsyncMock()
    return mocked_db, mocked_repository


@pytest.fixture
def app_service():
    return AppService()


# ================ test =================
@pytest.mark.anyio
async def test_app_service_update_app_success(setup, app_service: AppService):
    """ Test app service update app success  """
    # create a new application with valid data
    mocked_db, mocked_app_crud  = setup
    
    # mocked updated_data
    updated_data = dict(
        # set someting new
        applied_at = "Fri Aug 14 12:45:08 PM +0330 2026"
    )
    
    # mocked app_data 
    app_data = "test app"

    # mocked User
    mocked_user = Mock()
    mocked_user.id = 1
    
    # mocked found app
    mocked_found_app = Mock()
    mocked_found_app.user_id  = mocked_user.id # 1
    mocked_app_crud.get_app_by_title.return_value = mocked_found_app

    expected_update_app = Mock()
    expected_update_app.title = "test app"
    expected_update_app.applied_at =  "Fri Aug 14 12:45:08 PM +0330 2026"
    mocked_app_crud.update.return_value = expected_update_app
    
    result = await app_service.update(
        db= mocked_db,
        app_crud=  mocked_app_crud,
        app_data= app_data,
        updated_data=updated_data,
        user=  mocked_user
    ) 
    assert result is expected_update_app
    mocked_app_crud.get_app_by_title.assert_awaited_once
    mocked_app_crud.update.assert_awaited_once
    mocked_app_crud.get_app_by_id.assert_not_awaited
    mocked_app_crud.get_position_by_name.assert_not_awaited
    mocked_app_crud.get_status_by_name.assert_not_awaited
    mocked_app_crud.get_company_by_name.assert_not_awaited

@pytest.mark.anyio
async def test_app_service_update_app_fail_not_found_app(setup, app_service: AppService):
    """ Test app service update app fail the app not found  """
    # create a new application with valid data
    mocked_db, mocked_app_crud  = setup
    
    # mocked updated_data
    updated_data = dict(
        # set someting new
        applied_at = "Fri Aug 14 12:45:08 PM +0330 2026"
    )
    
    # mocked app_data 
    app_data = "test app"

    # mocked User
    mocked_user = Mock()
    mocked_user.id = 1
    
    # mocked found app
    mocked_found_app = Mock()
    mocked_found_app.user_id  = mocked_user.id # 1
    mocked_app_crud.get_app_by_title.return_value = None

    expected_update_app = Mock()
    expected_update_app.title = "test app"
    expected_update_app.applied_at =  "Fri Aug 14 12:45:08 PM +0330 2026"
    mocked_app_crud.update.return_value = expected_update_app
    
    with pytest.raises(HTTPException) as ex:
        await app_service.update(
            db= mocked_db,
            app_crud=  mocked_app_crud,
            app_data= app_data,
            updated_data=updated_data,
            user=  mocked_user
        ) 
        
    ex.value.status_code == 404
    ex.value.detail == "Application not found"
    
@pytest.mark.anyio
async def test_app_service_update_app_fail_user_not_have_access(setup, app_service: AppService):
    """ Test app service update app fail user not have access to this application  """
    # create a new application with valid data
    mocked_db, mocked_app_crud  = setup
    
    # mocked updated_data
    updated_data = dict(
        # set someting new
        applied_at = "Fri Aug 14 12:45:08 PM +0330 2026"
    )
    
    # mocked app_data 
    app_data = "test app"

    # mocked User
    mocked_user = Mock()
    mocked_user.id = 1
    
    # mocked found app
    mocked_found_app = Mock()
    mocked_found_app.user_id  = 2 # 2
    mocked_app_crud.get_app_by_title.return_value = mocked_found_app

    expected_update_app = Mock()
    expected_update_app.title = "test app"
    expected_update_app.applied_at =  "Fri Aug 14 12:45:08 PM +0330 2026"
    mocked_app_crud.update.return_value = expected_update_app
    
    with pytest.raises(HTTPException) as ex:
        await app_service.update(
            db= mocked_db,
            app_crud=  mocked_app_crud,
            app_data= app_data,
            updated_data=updated_data,
            user=  mocked_user
        ) 
        
    ex.value.status_code == 401
    ex.value.detail == "You do not have access to this application"

# ===================================== by id ==================================
@pytest.mark.anyio
async def test_app_service_update_app_success_by_id(setup, app_service: AppService):
    """ Test app service update app success  """
    # create a new application with valid data
    mocked_db, mocked_app_crud  = setup
    
    # mocked updated_data
    updated_data = dict(
        # set someting new
        applied_at = "Fri Aug 14 12:45:08 PM +0330 2026"
    )
    
    # mocked app_data 
    app_data = 1

    # mocked User
    mocked_user = Mock()
    mocked_user.id = 1
    
    # mocked found app
    mocked_found_app = Mock()
    mocked_found_app.user_id  = mocked_user.id # 1
    mocked_app_crud.get_app_by_id.return_value = mocked_found_app

    expected_update_app = Mock()
    expected_update_app.title = "test app"
    expected_update_app.applied_at =  "Fri Aug 14 12:45:08 PM +0330 2026"
    mocked_app_crud.update.return_value = expected_update_app
    
    result = await app_service.update(
        db= mocked_db,
        app_crud=  mocked_app_crud,
        app_data= app_data,
        updated_data=updated_data,
        user=  mocked_user
    ) 
    assert result is expected_update_app
    mocked_app_crud.get_app_by_id.assert_awaited_once
    mocked_app_crud.update.assert_awaited_once
    mocked_app_crud.get_app_by_title.assert_not_awaited
    mocked_app_crud.get_position_by_name.assert_not_awaited
    mocked_app_crud.get_status_by_name.assert_not_awaited
    mocked_app_crud.get_company_by_name.assert_not_awaited

@pytest.mark.anyio
async def test_app_service_update_app_fail_not_found_app_by_id(setup, app_service: AppService):
    """ Test app service update app by id fail the app not found  """
    # create a new application with valid data
    mocked_db, mocked_app_crud  = setup
    
    # mocked updated_data
    updated_data = dict(
        # set someting new
        applied_at = "Fri Aug 14 12:45:08 PM +0330 2026"
    )
    
    # mocked app_data 
    app_data = 1

    # mocked User
    mocked_user = Mock()
    mocked_user.id = 1
    
    # mocked found app
    mocked_found_app = Mock()
    mocked_found_app.user_id  = mocked_user.id # 1
    mocked_app_crud.get_app_by_title.return_value = None

    expected_update_app = Mock()
    expected_update_app.title = "test app"
    expected_update_app.applied_at =  "Fri Aug 14 12:45:08 PM +0330 2026"
    mocked_app_crud.update.return_value = expected_update_app
    
    with pytest.raises(HTTPException) as ex:
        await app_service.update(
            db= mocked_db,
            app_crud=  mocked_app_crud,
            app_data= app_data,
            updated_data=updated_data,
            user=  mocked_user
        ) 
        
    ex.value.status_code == 404
    ex.value.detail == "Application not found"
    
    
@pytest.mark.anyio
async def test_app_service_update_app_fail_user_not_have_access_by_id(setup, app_service: AppService):
    """ Test app service update app by id fail user not have access to this application  """
    # create a new application with valid data
    mocked_db, mocked_app_crud  = setup
    
    # mocked updated_data
    updated_data = dict(
        # set someting new
        applied_at = "Fri Aug 14 12:45:08 PM +0330 2026"
    )
    
    # mocked app_data 
    app_data = 1

    # mocked User
    mocked_user = Mock()
    mocked_user.id = 1
    
    # mocked found app
    mocked_found_app = Mock()
    mocked_found_app.user_id  = 2 # 2
    mocked_app_crud.get_app_by_title.return_value = mocked_found_app

    expected_update_app = Mock()
    expected_update_app.title = "test app"
    expected_update_app.applied_at =  "Fri Aug 14 12:45:08 PM +0330 2026"
    mocked_app_crud.update.return_value = expected_update_app
    
    with pytest.raises(HTTPException) as ex:
        await app_service.update(
            db= mocked_db,
            app_crud=  mocked_app_crud,
            app_data= app_data,
            updated_data=updated_data,
            user=  mocked_user
        ) 
        
    ex.value.status_code == 401
    ex.value.detail == "You do not have access to this application"

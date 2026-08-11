import pytest
from unittest.mock import AsyncMock, Mock, patch
from app.services.app import AppService

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
async def test_app_service_with_only_status(setup, app_service: AppService):
    """ Test app service create with only status  """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mock status
    mocked_get_status_by_name = Mock()
    mocked_get_status_by_name.id = 1
    mocked_repository.get_status_by_name.return_value = mocked_get_status_by_name

    # mock creation app 
    # -- This is for where the service check status 
    #     seted and is getting from databse. the object return is 
    #     the same as what we set in the mock.
    mocked_app_create = Mock()
    mocked_app_create.id  = 0
    mocked_app_create.user_id = 0
    mocked_app_create.title = "New Job Application"
    mocked_app_create.status =  1
    mocked_repository.create.return_value = mocked_app_create

    # ========= user Mock
    user_mock = Mock()
    user_mock.id = 0
    
    resp = await app_service.create(
        db=mocked_db,
        app_crud=mocked_repository,
        app_data={
            "title": "New Job Application",
            "status": "applied"
        },
        user=user_mock
    )
    # asserts
    finall_app_data={
        "title": "New Job Application",
        "status": 1,
        "user_id":0
    }
    mocked_repository.create.assert_awaited_once_with(
        mocked_db, finall_app_data
    )
    mocked_repository.get_status_by_name.assert_awaited_once_with(
        mocked_db, "applied"
    )
    assert resp.title  == finall_app_data["title"]
    assert resp.status == finall_app_data['status']
    assert resp.user_id == finall_app_data['user_id']
    
@pytest.mark.anyio
async def test_app_service_with_only_position(setup, app_service: AppService):
    """ Test if the service creates an application with only position data  """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mock status
    mocked_get_position_by_name = Mock()
    mocked_get_position_by_name.id = 1
    mocked_repository.get_position_by_name.return_value = mocked_get_position_by_name

    # mock creation app 
    mocked_app_create = Mock()
    mocked_app_create.id  = 0
    mocked_app_create.user_id = 0
    mocked_app_create.title = "New Job Application"
    mocked_app_create.position =  mocked_get_position_by_name.id
    mocked_repository.create.return_value = mocked_app_create

    # ========= user Mock
    user_mock = Mock()
    user_mock.id = 0
    resp = await app_service.create(
        db=mocked_db,
        app_crud=mocked_repository,
        app_data={
            "title": "New Job Application",
            "position": "Full-time"
        },
        user=user_mock
    )
    # asserts
    finall_app_data={
        "title": "New Job Application",
        "position": 1,
        "user_id":0
    }
    mocked_repository.create.assert_awaited_once_with(
        mocked_db, finall_app_data
    )
    mocked_repository.get_position_by_name.assert_awaited_once_with(
        mocked_db, "Full-time"
    )
    assert resp.title == finall_app_data.get('title')
    assert resp.position == finall_app_data.get('position')
    assert resp.user_id == finall_app_data.get("user_id")
    
@pytest.mark.anyio
async def test_app_service_with_only_job(setup, app_service: AppService):
    """ Test if the service creates an application with only job data  """
    # create a new application with valid data
    mocked_db, mocked_repository  = setup
    
    # mock status
    mocked_get_job_by_name = Mock()
    mocked_get_job_by_name.id = 1
    mocked_repository.get_job_by_name.return_value = mocked_get_job_by_name

    # mock creation app 
    mocked_app_create = Mock()
    mocked_app_create.id  = 0
    mocked_app_create.user_id = 0
    mocked_app_create.title = "New Job Application"
    mocked_app_create.job =  mocked_get_job_by_name.id
    mocked_repository.create.return_value = mocked_app_create

    # ========= user Mock
    user_mock = Mock()
    user_mock.id = 0    
    resp = await app_service.create(
        db=mocked_db,
        app_crud=mocked_repository,
        app_data={
            "title": "New Job Application",
            "job": "Software Engineer"
        },
        user=user_mock
    )
    # asserts
    finall_app_data={
        "title": "New Job Application",
        "job": 1,
        "user_id":0
    }
    mocked_repository.create.assert_awaited_once_with(
        mocked_db, finall_app_data
    )
    mocked_repository.get_job_by_name.assert_awaited_once_with(
        mocked_db,  "Software Engineer"
    )
    assert resp.title == finall_app_data.get('title')
    assert resp.job == finall_app_data.get('job')
    assert resp.user_id == finall_app_data.get('user_id')
    
@pytest.mark.anyio
async def test_app_service_with_status_job_position(setup, app_service: AppService):
    """ Test if the service creates an application with a job and a status and position """
    # setup
    mocked_db, mocked_repository  = setup
    
    # =========== job  ===========
    # mock job
    mocked_get_job_by_name = Mock()
    mocked_get_job_by_name.id = 1
    mocked_repository.get_job_by_name.return_value = mocked_get_job_by_name

    # =========== position ===========
    # mock position
    mocked_get_position_by_name = Mock()
    mocked_get_position_by_name.id = 1
    mocked_repository.get_position_by_name.return_value = mocked_get_position_by_name

    # ======== status ===========
    # mock status
    mocked_get_status_by_name = Mock()
    mocked_get_status_by_name.id = 1
    mocked_repository.get_status_by_name.return_value = mocked_get_status_by_name
    
    # ===== mock create app ========
    mocked_create_app = Mock()
    mocked_create_app.id  = 0
    mocked_create_app.user_id = 0
    mocked_create_app.title = "New Job Application"
    mocked_create_app.position = 1 
    mocked_create_app.status = 1
    mocked_create_app.job = 1
    mocked_repository.create.return_value = mocked_create_app
    
    # ========= user Mock
    user_mock = Mock()
    user_mock.id = 0    

    # =========== data we send to the service  ===========
    app_data={
        "title": "New Job Application",
        "job": "Software Engineer",
        "status":"applied",
        "position": "Full-time"
    }
    # ======== call the service method ========
    result = await app_service.create(
        mocked_db,
        mocked_repository,
        app_data,
        user_mock
    )
    # ======== assert the results ========
    assert result.title == "New Job Application"
    assert result.job == 1
    assert result.status == 1
    assert result.position == 1
    assert result.user_id == 0
    mocked_repository.create.assert_awaited_once_with(mocked_db,app_data)
    mocked_repository.get_job_by_name.assert_awaited_once_with(mocked_db,"Software Engineer")
    mocked_repository.get_position_by_name.assert_awaited_once_with(mocked_db,"Full-time")
    mocked_repository.get_status_by_name.assert_awaited_once_with(mocked_db,"applied")

@pytest.mark.anyio
async def test_app_service_with_invalid_company_given(app_service , setup):
    """ Test the app service with an invalid company name """
    from fastapi import HTTPException
    # ======== setup the mock repository and session ========
    mocked_db, mocked_repository  = setup
    
    # =========== job  ===========
    # mock job
    mocked_get_job_by_name = Mock()
    mocked_get_job_by_name.id = 1
    mocked_repository.get_job_by_name.return_value = mocked_get_job_by_name

    # =========== position ===========
    # mock position
    mocked_get_position_by_name = Mock()
    mocked_get_position_by_name.id = 1
    mocked_repository.get_position_by_name.return_value = mocked_get_position_by_name

    # ======== status ===========
    # mock status
    mocked_get_status_by_name = Mock()
    mocked_get_status_by_name.id = 1
    mocked_repository.get_status_by_name.return_value = mocked_get_status_by_name
    # =============== company  ===============
    # mock company
    mocked_repository.get_company_by_name.return_value = None
    
    # ======== create a sample application data ========
    import datetime
    app_data = dict(
        title="New Job Application",
        applied_at=datetime.datetime.now(),
        response_date=None,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        company="Invalid Company",
        job="Software Engineer",
        status="applied",
        position="Full-time"
    )
    
    user_mock = Mock()
    user_mock.id = 0   
    # ======== call the service method ========
    with pytest.raises(HTTPException) as exc_info:
        await app_service.create(
            mocked_db,
            mocked_repository,
            app_data,
            user=user_mock
        )
    # ======== assert the results ========
    assert exc_info.value.detail == f"Company with name {app_data.get("company")} not found"
    assert exc_info.value.status_code == 404
    mocked_repository.create.assert_not_awaited()
    mocked_repository.get_job_by_name.assert_not_awaited()
    mocked_repository.get_position_by_name.assert_not_awaited()
    mocked_repository.get_status_by_name.assert_not_awaited()
    
@pytest.mark.anyio
async def test_app_service_with_valid_company_given(app_service , setup):
    """ Test the app service with an valid company name """
    from fastapi import HTTPException
    # ======== setup the mock repository and session ========
    mocked_db, mocked_repository  = setup
    
    # =========== job  ===========
    # mock job
    mocked_get_job_by_name = Mock()
    mocked_get_job_by_name.id = 1
    mocked_repository.get_job_by_name.return_value = mocked_get_job_by_name

    # =========== position ===========
    # mock position
    mocked_get_position_by_name = Mock()
    mocked_get_position_by_name.id = 1
    mocked_repository.get_position_by_name.return_value = mocked_get_position_by_name

    # ======== status ===========
    # mock status
    mocked_get_status_by_name = Mock()
    mocked_get_status_by_name.id = 1
    mocked_repository.get_status_by_name.return_value = mocked_get_status_by_name
    # =============== company  ===============
    # mock company
    mocked_get_company_by_name = Mock()
    mocked_get_company_by_name.id = 1
    mocked_repository.get_company_by_name.return_value = mocked_get_company_by_name
    # =============== Mock create repository =================
    mocked_create_app = Mock()
    mocked_create_app.title ="New Job Application"
    mocked_create_app.user_id = 0
    mocked_create_app.company=1
    mocked_create_app.job=1
    mocked_create_app.status=1
    mocked_create_app.position=1
    mocked_repository.create.return_value = mocked_create_app
    # ======== create a sample application data ========
    import datetime
    app_data = dict(
        title="New Job Application",
        applied_at=datetime.datetime.now(),
        response_date=None,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        company="Valid Company",
        job="Software Engineer",
        status="applied",
        position="Full-time"
    )
    # ======== expected app data from response ========
    expected_app_data = dict(
        title="New Job Application",
        applied_at=app_data.get("applied_at"),
        response_date=None,
        created_at= app_data.get("created_at"),
        updated_at= app_data.get("updated_at"),
        user_id=0,
        company=1,
        job=1,
        status=1,
        position=1
    )
    
    user_mock = Mock()
    user_mock.id = 0   
    # ======== call the service method ========
    result  = await app_service.create(
        mocked_db,
        mocked_repository,
        app_data,
        user=user_mock
    )
    # ======== assert the results ========
    assert result.title == expected_app_data["title"]
    assert result.company == expected_app_data["company"]
    assert result.job == expected_app_data["job"]
    assert result.status == expected_app_data["status"]
    assert result.position == expected_app_data["position"]
    assert result.user_id == expected_app_data["user_id"]
    mocked_repository.create.assert_awaited_once_with(
        mocked_db , expected_app_data
    )
    mocked_repository.get_company_by_name.assert_awaited_once_with(
        mocked_db, "Valid Company"
    )
    mocked_repository.get_job_by_name.assert_awaited_once_with(
        mocked_db, "Software Engineer"
    )
    mocked_repository.get_position_by_name.assert_awaited_once_with(
        mocked_db, "Full-time"
    )
    mocked_repository.get_status_by_name.assert_awaited_once_with(
        mocked_db, "applied"
    )
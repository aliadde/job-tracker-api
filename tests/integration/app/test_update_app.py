import pytest
from app.schemas.app import CreateAppRequest

# =================================== fixtures ====================================================================
@pytest.fixture
def setup_(client):
    
    # create new user
    client.post("/auth/register",json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpass"
    })
    # login and get token
    resp = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    token = resp.json().get("access_token")
    return token

    
@pytest.fixture
def setup_2(client):
    
    # create new user
    client.post("/auth/register",json={
        "username": "testuser2",
        "email": "test2@test.com",
        "password": "testpass2"
    })
    # login and get token
    resp = client.post("/auth/login", json={
        "username": "testuser2",
        "password": "testpass2"
    })
    token = resp.json().get("access_token")
    return token


def create_app(token, cl):
    resp = cl.post(
        "/app",
        json={
        "title": "test app"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if resp.status_code == 201:
        return resp.json()
    else:
        raise Exception("Failed to create app")
    
@pytest.fixture
async def create_company():
    from tests.conftest import TestSessionLocal
    from app.models import Companies
    from app.repositories.company import CompanyRepository
    company_crud = CompanyRepository()
    async with TestSessionLocal() as db:
        test_company = Companies(name="testcompany")
        await company_crud.create(db, test_company)
        yield
        await company_crud.delete(db, test_company)
        
@pytest.fixture
async def get_status_id():
    # get id of applied from real dtabase for assertion
    from tests.conftest import TestSessionLocal
    from app.repositories.app import AppRepository
    
    app_crud = AppRepository()
    async with TestSessionLocal() as session:
        status_id = await app_crud.get_status_by_name(db=session, status="applied")
        return status_id.id

@pytest.fixture
async def get_job_id():
    # get id of applied from real dtabase for assertion
    from tests.conftest import TestSessionLocal
    from app.repositories.app import AppRepository
    
    app_crud = AppRepository()
    async with TestSessionLocal() as session:
        job = await app_crud.get_job_by_name(db=session,title="Software Engineer")
        return job.id

@pytest.fixture
async def get_position_id():
    # get id of applied from real dtabase for assertion
    from tests.conftest import TestSessionLocal
    from app.repositories.app import AppRepository
    
    app_crud = AppRepository()
    async with TestSessionLocal() as session:
        position = await app_crud.get_position_by_name(db=session,position="Full-time")
        return position.id
# =================================== tests ======================================================================
@pytest.mark.anyio
async def test_update_an_app_by_title(setup_,client):
    """ 
    update an app with title of taht app .
    update: applied_at field
    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    update_data = dict(
        applied_at="2023-04-01T12:00:00Z"
    )
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == 200
    assert response_update.json().get("id") == app.get("id")
    assert response_update.json().get("title") == app.get("title")
    assert response_update.json().get("applied_at") == "2023-04-01T12:00:00Z"
    
@pytest.mark.anyio
async def test_update_an_app_by_title_with_all_fields(setup_, client, create_company):
    """ 
    update an app by title. 
    update fileds with all fields.
    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    update_data = dict(
        title= "updated title",
        applied_at= "2023-04-01T12:00:00Z",
        response_date= "2025-04-01T12:00:00Z",
        status ="applied",
        position = "Full-time",
        job = "Software Engineer",
        company = "testcompany"
    )
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == 200
    assert response_update.json().get("id") == app.get("id")


@pytest.mark.anyio
async def test_update_an_app_by_title_with_company_fields(setup_, client, create_company):
    """ 
    update an app by title. 
    update company field.
    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    update_data = dict(
        company = "testcompany"
    )
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == 200
    assert response_update.json().get("id") == app.get("id")
    assert response_update.json().get("company_id") == 1
    
@pytest.mark.anyio
async def test_update_an_app_by_title_with_status_field(setup_, client, get_status_id, create_company):
    """ 
    update an app by title. 
    update fileds with status field.
    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    update_data = dict(
        status ="applied",
    )
    # applied status id 
    applied_status_id = get_status_id
    
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == 200
    assert response_update.json().get("id") == app.get("id")
    assert response_update.json().get("status_id") == applied_status_id

@pytest.mark.anyio
async def test_update_an_app_by_title_with_job_field(setup_, get_job_id, client, create_company):
    """ 
    update an app by title. 
    update fileds with all fields.
    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    update_data = dict(
        job = "Software Engineer"
    )
    software_engineer_job_id = get_job_id
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == 200
    assert response_update.json().get("id") == app.get("id")
    assert response_update.json().get("job_id") == software_engineer_job_id

@pytest.mark.anyio
async def test_update_an_app_by_title_with_position_fields(setup_, get_position_id, client, create_company):
    """ 
    update an app by title. 
    update fileds with positon
    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    update_data = dict(
        position = "Full-time"
    )
    full_time_possition_id = get_position_id
    
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == 200
    assert response_update.json().get("id") == app.get("id")
    assert response_update.json().get("position_id") == full_time_possition_id

@pytest.mark.anyio
async def test_update_an_app_by_title_with_all_fields_fail_wrong_app_title(setup_, client, create_company):
    """ 
    update an app by title. but fail becuase wrong title 
    update fileds with all fields.

    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title") + "11" # cause of fail
    assert app_title is not None
    update_data = dict(
        title= "updated title",
        applied_at= "2023-04-01T12:00:00Z",
        response_date= "2025-04-01T12:00:00Z",
        status ="applied",
        position = "Full-time",
        job = "Software Engineer",
        company = "testcompany"
    )
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_update.status_code == 404
    assert response_update.json().get("detail") == "Application not found"
    
@pytest.mark.anyio
async def test_update_an_app_by_title_with_all_fields_fail_not_access_by_this_user(setup_, setup_2, client, create_company):
    """ 
    update an app by title. but fail because user not have access  to this app
    fileds:
    update fileds with all fields.
    """
    token = setup_
    token_user_2 = setup_2
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    update_data = dict(
        title= "updated title",
        applied_at= "2023-04-01T12:00:00Z",
        response_date= "2025-04-01T12:00:00Z",
        status ="applied",
        position = "Full-time",
        job = "Software Engineer",
        company = "testcompany"
    )
    response_update = client.patch(
        f'/app/update/{app_title}', 
        json=update_data,
        headers={'Authorization': f'Bearer {token_user_2}'}
    )

    assert response_update.status_code == 401
    assert response_update.json().get("detail") == "You do not have access to this application"
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


def create_app(token, cl, app_title: str):
    resp = cl.post(
        "/app",
        json={
        "title": app_title
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
async def test_get_all_app(setup_,client):
    """ 
    Test get all apps for authenticated user.
    """
    token = setup_
    
    app1 = create_app(token, client, "app test1")
    app2 = create_app(token, client, "app test2")
    app3 = create_app(token, client, "app test3")
    created_app_list = [
        app1, app2, app3
    ]

    response_get_all = client.get(
        f'/app/all', 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_get_all.status_code == 200
    assert type(response_get_all.json()) == list
    for app,created_app in zip(response_get_all.json(), created_app_list):
        assert app == created_app
        
@pytest.mark.anyio
async def test_get_all_apps_no_app_exist(setup_,client):
    """ 
    Test get all apps but not app exist.
    """
    token = setup_

    response_get_all = client.get(
        f'/app/all', 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_get_all.status_code == 200
    assert type(response_get_all.json()) == list
    assert len(response_get_all.json()) == 0
import pytest
from app.schemas.app import CreateAppRequest

# =================================== fixtures ===================================
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
def change_expiration():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    old_value = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = str(1 / 60) # 1 Secound
    yield

    if old_value is not None:
        os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = old_value
    else:
        del os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]

@pytest.fixture
async def remove_user():
    from tests.conftest import TestSessionLocal
    from sqlalchemy import text
    async with TestSessionLocal() as db:
        await db.execute(text("DELETE FROM users WHERE username='testuser'"))
        await db.commit()


@pytest.fixture
async def create_company():
    from tests.conftest import TestSessionLocal
    from app.models import Companies
    from app.repositories.company import CompanyRepository
    company_crud = CompanyRepository()
    async with TestSessionLocal() as db:
        test_company = Companies(name="testcompany")
        await company_crud.create(db, test_company)
    
# =================================== tests ===================================
@pytest.mark.anyio
async def test_create_new_app_success(setup_, client): 
    
    token = setup_

    new_app = dict(
        title="test app",
        applied_at=None,
        response_date=None,
        company=None,
        status=None,
        position=None,
        job=None
    )
    print(new_app)
    result = client.post(
        "/app",
        headers={"Authorization": f"Bearer {token}"},
        json=new_app
    )
    # assertions
    assert result.status_code == 201
    result.json().get("title") == "test app"
    result.json().get("user_id") == 1
    result.json().get("id") == 1
    result.json().get("applied_at") == None
    result.json().get("response_date") == None
    result.json().get("company") == None
    result.json().get("status") == None
    result.json().get("position") == None
    result.json().get("job") == None
    result.json().get("created_at") is not None
    result.json().get("updated_at") is not None
    
@pytest.mark.anyio
async def test_create_new_app_fail_invalid_token(setup_, client): 
    """ token is invalid """
    token = setup_
    # change token
    token += "11"
    
    new_app = dict(
        title="test app",
        applied_at=None,
        response_date=None,
        company=None,
        status=None,
        position=None,
        job=None
    )
    print(new_app)
    result = client.post(
        "/app",
        headers={"Authorization": f"Bearer {token}"},
        json=new_app
    )
    # assertions
    assert result.status_code == 401
    result.json().get("detail") == "Invalid token"
    
@pytest.mark.anyio
async def test_create_new_app_failur_expire_token(change_expiration, setup_, client): 
    """ token expired """
    import time 
    token = setup_

    new_app = dict(
        title="test app",
        applied_at=None,
        response_date=None,
        company=None,
        status=None,
        position=None,
        job=None
    )

    time.sleep(2)
    result = client.post(
        "/app",
        headers={"Authorization": f"Bearer {token}"},
        json=new_app
    )
    # assertions
    assert result.status_code == 401
    result.json().get("detail") == "Token has expired"
    
@pytest.mark.anyio
async def test_create_new_app_user_removed_not_exist(setup_, remove_user, client): 
    """ user register, login and revcive token. but immedialtly removed """
    token = setup_

    new_app = dict(
        title="test app",
        applied_at=None,
        response_date=None,
        company=None,
        status=None,
        position=None,
        job=None
    )
    print(new_app)
    result = client.post(
        "/app",
        headers={"Authorization": f"Bearer {token}"},
        json=new_app
    )
    # assertions
    assert result.status_code == 404
    result.json().get("title") == "User not found"

@pytest.mark.anyio
async def test_create_new_app_company_not_found(setup_, client): 
    
    token = setup_

    new_app = dict(
        title="test app",
        applied_at=None,
        response_date=None,
        company="invalid company",
        status=None,
        position=None,
        job=None
    )
    print(new_app)
    result = client.post(
        "/app",
        headers={"Authorization": f"Bearer {token}"},
        json=new_app
    )
    # assertions
    assert result.status_code == 404
    result.json().get("detail") == f"Company with name {new_app.get("company")} not found"
    
@pytest.mark.anyio
async def test_create_new_app_company_is_exist(setup_, client, create_company): 
    """ test create new app when company is exist in database """
    token = setup_

    new_app = dict(
        title="test app",
        applied_at=None,
        response_date=None,
        company="testcompany",
        status=None,
        position=None,
        job=None
    )

    result = client.post(
        "/app",
        headers={"Authorization": f"Bearer {token}"},
        json=new_app
    )
    # assertions
    assert result.status_code == 201
    assert result.json().get("title") == new_app.get("title")
    assert result.json().get("id") == 1
    assert result.json().get("user_id") == 1
    assert result.json().get("applied_at") is None
    assert result.json().get("response_date") is None
    assert result.json().get("company_id") == 1
    assert result.json().get("status_is") is None
    assert result.json().get("position_id") is None
    assert result.json().get("job_id") is None
    
@pytest.mark.anyio
async def test_create_new_app_company_completly_all_fields(setup_, client, create_company): 
    """ test create new app when company is exist in database ex
    the creation is with all fields exepction of response_date and applied_at
    """
    token = setup_

    new_app = dict(
        title="test app",
        applied_at=None,
        response_date=None,
        company="testcompany",
        status="applied",
        position="Full-time",
        job="Software Engineer"
    )

    result = client.post(
        "/app",
        headers={"Authorization": f"Bearer {token}"},
        json=new_app
    )
    # assertions
    assert result.status_code == 201
    assert result.json().get("title") == new_app.get("title")
    assert result.json().get("id") == 1
    assert result.json().get("user_id") == 1
    assert result.json().get("applied_at") is None
    assert result.json().get("response_date") is None
    assert result.json().get("company_id") == 1
    assert result.json().get("status_id") == 1
    assert result.json().get("position_id") == 1
    assert result.json().get("job_id") == 1
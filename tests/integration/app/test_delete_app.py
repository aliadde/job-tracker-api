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

# =================================== tests ======================================================================
@pytest.mark.anyio
async def test_delete_an_app_by_id(setup_,client):
    token = setup_
    
    app = create_app(token, client)
    app_id  = app.get("id")
    assert app_id is not None
    
    response_delete = client.delete(
        f'/app/id/{app_id}', 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_delete.status_code == 200
    assert response_delete.json().get("id") == 1
    app = create_app(token, client)
    assert response_delete.json().get("title") == "test app"
    

@pytest.mark.anyio
async def test_delete_an_app_by_title(setup_,client):
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    assert app_title is not None
    
    response_delete = client.delete(
        f'/app/title/{app_title}', 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_delete.status_code == 200
    assert response_delete.json().get("id") == 1
    assert response_delete.json().get("title") == "test app"
    

@pytest.mark.anyio
async def test_delete_an_app_by_title_failur_wrong_title(setup_,client):
    """ 
    delete an app by title, but title is incorrect or not found in database
    """
    token = setup_
    
    app = create_app(token, client)
    app_title  = app.get("title")
    app_title += "11" # add some mess
    assert app_title is not None
    
    response_delete = client.delete(
        f'/app/title/{app_title}', 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_delete.status_code == 404
    assert response_delete.json().get('detail') == "Application not found"
    
    
@pytest.mark.anyio
async def test_delete_an_app_by_id_failur_wrong_id(setup_,client):
    """ 
    delete an app by id, but id is incorrect or not found in database
    """
    token = setup_
    
    app = create_app(token, client)
    app_id  = app.get("id")
    app_id += 1 # add some mess
    assert app_id is not None
    
    response_delete = client.delete(
        f'/app/title/{app_id}', 
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response_delete.status_code == 404
    assert response_delete.json().get('detail') == "Application not found"
        
    
@pytest.mark.anyio
async def test_delete_an_app_by_title_failur_wrong_user(setup_, setup_2, client):
    """ 
    delete an app by title, but user is not valid user for this application

    test explaination:
    we create two user. then create an app by user 1,
    then user2 send request to delete an app by title that owns by user1
    """
    token_user1 = setup_
    token_user2 = setup_2
    app = create_app(token_user1, client)
    app_title  = app.get("title")
    assert app_title is not None
    
    response_delete = client.delete(
        f'/app/title/{app_title}', 
        headers={'Authorization': f'Bearer {token_user2}'}
    )

    assert response_delete.status_code == 401
    assert response_delete.json().get('detail') == "You do not have access to this application"
    

@pytest.mark.anyio
async def test_delete_an_app_by_id_failur_wrong_user(setup_, setup_2, client):
    """ 
    delete an app by id, but user is not valid user for this application

    test explaination:
    we create two user. then create an app by user 1,
    then user2 send request to delete an app by id that owns by user1
    """
    token_user1 = setup_
    token_user2 = setup_2
    app = create_app(token_user1, client)
    app_id  = app.get("id")
    assert app_id is not None
    
    response_delete = client.delete(
        f'/app/id/{app_id}', 
        headers={'Authorization': f'Bearer {token_user2}'}
    )

    assert response_delete.status_code == 401
    assert response_delete.json().get('detail') == "You do not have access to this application"
    

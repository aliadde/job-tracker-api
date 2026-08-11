import pytest_asyncio, pytest

def test_integration_registeration_success(client):
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testuserpassword"
    }
    
    response = client.post("/auth/register", json=user_data)
    print(response.json())
    
    assert response.status_code == 201
    assert response.json().get("id") == 1
    assert response.json().get("username") == user_data.get("username")
    assert response.json().get("email") == user_data.get("email")
    assert response.json().get("password") != user_data.get("password")
    
    
@pytest_asyncio.fixture
async def db_session():
    import tests.conftest as conftest
    
    async with conftest.TestSessionLocal() as session:
        yield session

@pytest.mark.asyncio     
async def test_registeration_failure_same_email_with_db_commit(db_session, client):

    from app.models.users import Users
    user  = Users(
        username="testuser1",
        email="test@example.com",
        hashed_password="testuserpassword1"
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    user_data = {
        "username": "testuser2",
        "email": "test@example.com",
        "password": "testuserpassword2"
    }
    
    response = client.post("/auth/register", json=user_data)
    print(response.json())
    
    assert response.status_code == 409
    assert response.json() == {"detail": "Email already exists"}

def test_registeration_failure_same_email_with_api_requests(client):
    user1  = {
        "username":"testuser1",
        "email":"test@example.com",
        "password":"testuserpassword1"
    }
    response = client.post("/auth/register", json=user1)
    
    user2= {
        "username":"testuser2",
        "email":"test@example.com",
        "password":"testuserpassword2"
    }
    
    response2 = client.post("/auth/register", json=user2)
    
    
    assert response2.status_code == 409
    assert response2.json() == {"detail": "Email already exists"}
    
def test_register_short_name(client):
    user_data = { 
        "username": "ts",  # the usernaem is to  short
        "email": "test@example.com",
        "password": "testuserpassword"
    }
    response = client.post('/auth/register',json=user_data)
    assert response.status_code == 422

def test_register_baad_email(client):
    user_data = { 
        "username": "testuser",  
        "email": "test@", # the email is not correct style 
        "password": "testuserpassword"
    }
    res1 = client.post('/auth/register',json=user_data)
    assert res1.status_code == 422
    
    user_data2 = { 
        "username": "testuser",  
        "email": "test@gmail.", # the email is not correct style 
        "password": "testuserpassword"
    }
    res2 = client.post('/auth/register',json=user_data2)
    assert res2.status_code == 422
    
    user_data3 = { 
        "username": "testuser",  
        "email": "@gmail.com", # the email is not correct style 
        "password": "testuserpassword"
    }
    res3 = client.post('/auth/register',json=user_data3)
    assert res3.status_code == 422
    
    
def test_register_short_name(client):
    user_data = { 
        "username": "testuser",  
        "email": "test@example.com",
        "password": "J7x0o7d" # the password is to  short (< 8)
    }
    response = client.post('/auth/register',json=user_data)
    assert response.status_code == 422
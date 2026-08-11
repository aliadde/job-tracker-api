import  pytest
from fastapi import HTTPException

@pytest.fixture()
def create_user(client):
    # ----
    # create user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testuserpassword"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201

    return user_data
    # ----

def test_integration_login_success(client, create_user):
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testuserpassword"
    }
    
    response_login = client.post("/auth/login", json={"username":user_data.get("username"), 
                                                 "password": user_data.get("password")})
        
    assert response_login.status_code == 200
    assert response_login.json().get("access_token")  is not None
    assert response_login.json().get("token_type") == "bearer"
    

def test_integration_login_failur_username(client, create_user):
    
    user_data = {
        "username": "stuser",
        "email": "test@example.com",
        "password": "testuserpassword"
    }

    response_login = client.post("/auth/login", 
        json={"username":user_data.get("username"), "password": user_data.get("password")})
        
    
    assert response_login.status_code == 404
    assert response_login.json()["detail"] == "invalid username or password"

    
def test_integration_login_failur_password(client, create_user):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testuserpassw"
    }

    response_login = client.post("/auth/login", 
        json={"username":user_data.get("username"), "password": user_data.get("password")})
        
    
    assert response_login.status_code == 404
    assert response_login.json()["detail"] == "invalid username or password"


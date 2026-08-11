import pytest

@pytest.fixture
def create_user(client):
    user = {
        "username":"testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    # register a user
    response = client.post("/auth/register", json=user)
    
    # now login to get jwt-token
    login_response = client.post("/auth/login", json={"username":"testuser","password":"testpassword"})
    return login_response.json().get("access_token")


def test_get_current_usr_success(client, create_user):
    access_token = create_user
    
    # Now send request get request to end point /auth/current_user with Barear token set
    response = client.get("/auth/current_user", headers={"Authorization": f"Bearer {access_token}"})
    
    # now write assertion for response
    assert response.status_code == 200
    assert response.json().get("username") == "testuser"
    assert response.json().get("email") == "test@example.com"
    assert response.json().get("is_active") == True
    
def test_get_current_usr_failure(client, create_user):
    ...
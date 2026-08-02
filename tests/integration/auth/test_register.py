import pytest


def test_integration_registeration_success(client):
    
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testuserpassword"
    }
    
    response = client.post("/register", json=user_data)
    
    assert response.status_code == 201
    user_data["id"] = 1
    assert user_data in response.json()
    

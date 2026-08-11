import pytest

@pytest.fixture()
def exp_change():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    old_value = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = str(1 / 60)
    yield

    if old_value is not None:
        os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = old_value
    else:
        del os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]

@pytest.fixture(scope="function")
def create_user(client):
    client.post('/auth/register', json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass"
    })
    token = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    return token.json()

def test_token_expired(exp_change, create_user, client ):
    """ 
    The expiration of token is under 1.5 secound.
    """
    token = create_user
    from fastapi import HTTPException
    from  time import sleep
    
    sleep(1.5)
    res = client.get("/auth/current_user", headers={"Authorization": f"Bearer {token['access_token']}"})
    
        
    assert res.status_code == 401
    assert res.json().get("detail") == "Token has expired"
    
def test_token_invalid(create_user, client):
    """ 
    The token is invalid.
    """
    token = create_user
    # a little change on token will rak it
    token["access_token"] = token.get("access_token") + "1234"
    from fastapi import HTTPException
    from  time import sleep
    
    res = client.get("/auth/current_user", headers={"Authorization": f"Bearer {token['access_token']}"})
    
    assert res.status_code == 401
    assert res.json().get("detail") == "Invalid token"
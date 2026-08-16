import pytest
from tests.conftest import TestSessionLocal
from sqlalchemy import select
from app.models.users import Users
import app.core.security as security
# =================== fuxture ========================
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
    login_response = client.post(
        "/auth/login",
        json={
            "username":"testuser",
            "password":"testpassword"
        }
    )
    return login_response.json().get("access_token")



# =================== test ===========================
@pytest.mark.anyio
async def test_update_current_user_success(create_user, client):
    token:str = create_user
    
    update_data = dict(
        username="testuser_updated_name",
        email="testuser_updated_email@gmail.com",
        password="testuser_updated_password",
    )
    
    response_update =client.patch(
        "/auth/update",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_update_js = response_update.json() 
    assert response_update.status_code == 200
    assert response_update_js.get("username") == update_data.get("username")
    assert response_update_js.get("email") == update_data.get("email")
    assert response_update_js.get("hashed_password") is None
    assert response_update_js.get("password") is None
    
    # real check the datbase
    async with TestSessionLocal() as db:
        stm = select(Users).where(Users.username == update_data.get("username") )
        result = await db.execute(stm)
        user:Users = result.scalars().first()
    
    assert user.username == update_data.get("username")
    assert user.email == update_data.get("email")
    assert user.hashed_password != update_data.get("password")
    assert security.verify_password(
        password= update_data.get("password"),
        hashed_password=user.hashed_password
    ) is True
    
@pytest.mark.anyio
async def test_update_current_user_only_username_success(create_user, client):
    token:str = create_user
    
    update_data = dict(
        username="testuser_updated_name",
    )
    
    response_update =client.patch(
        "/auth/update",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_update_js = response_update.json() 
    assert response_update.status_code == 200
    assert response_update_js.get("username") == update_data.get("username")
    assert response_update_js.get("hashed_password") is None
    assert response_update_js.get("password") is None
    
    # real check the datbase
    async with TestSessionLocal() as db:
        stm = select(Users).where(Users.username == update_data.get("username") )
        result = await db.execute(stm)
        user:Users = result.scalars().first()
    
    assert user.username == update_data.get("username")
    
@pytest.mark.anyio
async def test_update_current_user_only_password_success(create_user, client):
    token:str = create_user
    
    update_data = dict(
        password="testuser_updated_password",
    )
    
    response_update =client.patch(
        "/auth/update",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    response_update_js = response_update.json() 
    assert response_update.status_code == 200
    assert response_update_js.get("hashed_password") is None
    assert response_update_js.get("password") is None
    
    # real check the datbase
    async with TestSessionLocal() as db:
        stm = select(Users).where(Users.username == response_update_js.get("username") )
        result = await db.execute(stm)
        user:Users = result.scalars().first()
    
    assert hasattr(user, "hashed_password") is True
    assert hasattr(user, "password") is False
    assert security.verify_password(
        password= update_data.get("password"),
        hashed_password=user.hashed_password
    ) is True


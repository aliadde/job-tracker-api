import pytest
from app.models.users import Users

# ================== Fixture ===============
@pytest.fixture
def setup(client)-> Users:
    user_data = {
        "username":"testuser",
        "email":"testuser@gmail.com",
        "password":"testuser123",
    }
    result = client.post(
        "/auth/register", 
        json=user_data,
    )
    if result.status_code != 201:
        raise Exception(
            "in Setup fixture. we couldn't create a user."
        )

    result2 = client.post(
        "/auth/login", 
        json=dict(
            username=user_data.get("username"),
            password=user_data.get("password"),
        )
    )
    if result2.status_code != 200:
        raise Exception(
            "in Setup fixture.we couldn't login."
        )

    return result.json(), result2.json().get("access_token")

# ================== Test ==================
@pytest.mark.anyio
async def test_delete_user_success(setup, client):
    """Delete currest user logged in."""
    user, token = setup
    resp = client.delete(
        "/auth/delete",
        headers={"Authorization": f"Bearer {token}"},
    )

    result_user :dict = resp.json()

    assert resp.status_code == 200
    assert result_user.get("id") == user.get("id")
    assert result_user.get("username") == user.get("username")
    assert result_user.get("email") == user.get("email")


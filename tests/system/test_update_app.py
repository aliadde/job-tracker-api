import pytest
import datetime

@pytest.fixture
def create_company(client):
    client.post(
        '/metadata/company',
        json=dict(
            name="google"
        )
    )


def test_update_diffrent_field(client, create_company):

# ====================================================================
    # 1. Register
    register_response = client.post(
        "/auth/register",
        json={
            "username": "systemuser3",
            "email": "system3@example.com",
            "password": "systempassword3",
        },
    )

# ====================================================================
    # 2. Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": "systemuser3",
            "password": "systempassword3",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    #  Authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }

# ====================================================================
    # 3. create app
    create_res = client.post(
        '/app',
        json=dict(
            title="app",
            job="Software Engineer",
            status="applied",
            position='Full-time',
        ),
        headers=headers
    )
    assert create_res.status_code == 201
    
# ====================================================================
    # 4. update app (company )
    update_app_add_company_res = client.patch(
        '/app/update/title/app',
        json=dict(
            company="google"
        ),
        headers=headers,
    )
    assert update_app_add_company_res.status_code == 200
    assert update_app_add_company_res.json().get("company_id") == 1
    
# ====================================================================
    # 5. update app (applied at)
    applied_at = str(datetime.datetime.now())
    update_app_add_applied_at_res = client.patch(
        '/app/update/title/app',
        json=dict(
            applied_at=applied_at,
        ),
        headers=headers,
    )
    assert update_app_add_applied_at_res.status_code == 200
    assert update_app_add_applied_at_res.json().get("applied_at") is not None

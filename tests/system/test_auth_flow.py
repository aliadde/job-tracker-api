def test_create_and_get_application(client):

# ====================================================================
    # 1. Register
    register_response = client.post(
        "/auth/register",
        json={
            "username": "systemuser",
            "email": "system@example.com",
            "password": "systempassword",
        },
    )

    assert register_response.status_code == 201

# ====================================================================
    # 2. Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": "systemuser",
            "password": "systempassword",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3. Authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }
# ====================================================================
    # 4. Create application
    application_response = client.post(
        "/app",
        json=dict(
            title='test app1',
            status='applied',
            job='Software Engineer',
            position='Full-time'
        ),
        headers=headers,
    )

    assert application_response.status_code == 201

    application = application_response.json()

    application_id = application["id"]

# ====================================================================
    # 5. Get application
    get_response = client.get(
        f"/app/id/{application_id}",
        headers=headers,
    )

    assert get_response.status_code == 200

    result = get_response.json()

    assert result["id"] == application_id

def test_get_all_app(client):
# ====================================================================
    # 2. Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": "systemuser",
            "password": "systempassword",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3. Authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }
# ====================================================================
    # 4. Create application
    application_response = client.post(
        "/app",
        json=dict(
            title='test app1',
            status='applied',
            job='Software Engineer',
            position='Full-time'
        ),
        headers=headers,
    )

    assert application_response.status_code == 201

    application = application_response.json()

    application_id = application["id"]

# ====================================================================
    # 5. Get application
    get_response = client.get(
        f"/app/all",
        headers=headers,
    )

    assert get_response.status_code == 200

    result = get_response.json()

    assert isinstance(result , list)

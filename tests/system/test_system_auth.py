def test_all_auth(client):
    """
    register --> login --> current_user -->
    update user --> current_user --> delete user
    --> login [fail]

    """

# ====================================================================
    # 1. Register
    register_response = client.post(
        "/auth/register",
        json={
            "username": "systemuser2",
            "email": "system2@example.com",
            "password": "systempassword2",
        },
    )


# ====================================================================
    # 2. Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": "systemuser2",
            "password": "systempassword2",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # 3. Authorization header
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
# ====================================================================
    # 3. current user
    get_current_user_1_res = client.get(
        "/auth/current_user",
        headers=headers
    )
    assert get_current_user_1_res.status_code == 200
    
# ======~==============================================================
    # 4. update user
    update_user_res = client.patch(
            "/auth/update",
            json={
                "email":"testuser_updated_email@gmail.com"
            },
            headers=headers
        )
    assert update_user_res.status_code == 200
    
# ====================================================================
    # 5. current user
    get_current_user_2_res = client.get(
        "/auth/current_user",
        headers=headers
    )
    assert get_current_user_2_res.status_code == 200
    assert get_current_user_2_res.json().get("email") == "testuser_updated_email@gmail.com"

# ====================================================================
    # 6. delete user
    delete_user_res = client.delete(
        "/auth/delete",
        headers=headers
    )
    assert delete_user_res.status_code == 200

# ====================================================================
    # 7. get current user failiru
    get_current_user_3_res = client.get(
        "/auth/current_user",
        headers=headers
    )
    assert get_current_user_3_res.status_code == 404
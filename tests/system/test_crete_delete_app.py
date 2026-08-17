
def test_create_10_app_delete_10_app(client):

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
    
    title_list: list = [
        f"app{i}" for i in range(1,11)
    ]
    
    # create app
    for title in title_list:
        create_res = client.post(
            '/app',
            json={
                "title": f"{title}",
            },
            headers=headers
        )
        assert create_res.status_code == 201
        
        
    # delete by title
    for title in title_list:
        delete_res = client.delete(
            f'/app/title/{title}',
            headers=headers,
        )
        assert delete_res.status_code == 200
        
    get_all_res = client.get(
        '/app/all',
        headers=headers
    )
    assert get_all_res.status_code == 200
    assert isinstance(get_all_res.json(), list)
    assert len(get_all_res.json()) == 0

def test_create_update_app_delete(client):
    """
    create app
    update app
    get app and check updated or not 
    get all app and check : list have one element and that element is exact same
    delete app
    get all app an must be zero in list
    """
    
    
# ============================== login ======================================
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
# ================================= create app ===================================
    create_res = client.post(
        "/app",
        json={
            "title":"app1"
        },
        headers=headers
    )
    assert create_res.status_code == 201
    app_id = create_res.json().get("id")

# ================================ update app ====================================
    update_res = client.patch(
        "/app/update/title/app1",
        json={
            "title":"app2",
            "status":"applied",
            "position":"Full-time",
        },
        headers=headers
    )

    assert update_res.status_code == 200

# =========================== get that app =========================================
    get_app_res = client.get(
        f'/app/id/{app_id}',
        headers=headers,
    )
    assert get_app_res.status_code == 200
    assert get_app_res.json().get("id") == app_id
    assert get_app_res.json().get("title") == "app2"
    assert get_app_res.json().get("status_id") == 1
    assert get_app_res.json().get("position_id") == 1
    
# ================================= get all app ===================================
    get_all_res = client.get(
        '/app/all',
        headers=headers
    )
    assert get_all_res.status_code == 200
    assert len(get_all_res.json()) == 1
    assert get_all_res.json()[0].get("id") == app_id
    assert get_all_res.json()[0].get("title") == 'app2'
# ================================= delete app ===================================
    delete_res = client.delete(
        f'/app/id/{app_id}',
        headers=headers,
    )
    assert delete_res.status_code  == 200
    assert delete_res.json().get('id') == app_id
# ================================= get all app ===================================
    # must be empty
    empty_get_all_res = client.get(
        '/app/all',
        headers=headers
    )
    assert empty_get_all_res.status_code == 200
    assert len(empty_get_all_res.json()) == 0

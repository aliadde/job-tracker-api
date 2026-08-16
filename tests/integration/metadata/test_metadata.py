import pytest

# ============================== test =========================
@pytest.mark.anyio
async def test_get_all_statuses(client):
    
    response = client.get("/metadata/status")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
@pytest.mark.anyio
async def test_get_all_jobs(client):
    
    response = client.get("/metadata/job")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
@pytest.mark.anyio
async def test_get_all_positions(client):
    
    response = client.get("/metadata/position")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
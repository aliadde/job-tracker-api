import httpx
import pytest
import subprocess

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL) as client:
        yield client

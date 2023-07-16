import httpx
import pytest
from uuid import uuid4

@pytest.mark.asyncio
async def test_sign_new_user(client: httpx.AsyncClient) -> None:
    unique_email = f"testuser_{uuid4()}@packt.com"
    payload = {
        "email": unique_email,
        "password": "testpassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    test_response = {
        "message": "User created successfully.",
    }
    response = await client.post("/user/signup", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response

@pytest.mark.asyncio
async def test_sign_user_in(client: httpx.AsyncClient) -> None:
    unique_email = f"testuser_{uuid4()}@packt.com"
    payload = {
        "username": unique_email,
        "password": "testpassword",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await client.post("/user/login", data=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"
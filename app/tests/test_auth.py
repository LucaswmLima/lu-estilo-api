import pytest
from httpx import AsyncClient
from app.core.config import BASE_URL

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(base_url=BASE_URL) as ac:
        response = await ac.post("/auth/register", json={"email": "test@example.com", "password": "senha123"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_register_duplicate_user():
    async with AsyncClient(base_url=BASE_URL) as ac:
        await ac.post("/auth/register", json={"email": "testdup@example.com", "password": "senha123"})
        response = await ac.post("/auth/register", json={"email": "testdup@example.com", "password": "senha123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

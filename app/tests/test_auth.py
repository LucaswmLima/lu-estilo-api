import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json={"email": "test@example.com", "password": "senha123"})
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_register_duplicate_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # registra usuário uma vez
        await ac.post("/auth/register", json={"email": "testdup@example.com", "password": "senha123"})
        # tenta registrar de novo (deve dar erro)
        response = await ac.post("/auth/register", json={"email": "testdup@example.com", "password": "senha123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

import pytest
from httpx import AsyncClient
from app.core.config import BASE_URL

@pytest.mark.asyncio
async def test_user_register_login_and_delete():
    async with AsyncClient(base_url=BASE_URL) as ac:
        # 1. Registra o usuário
        register_response = await ac.post("/auth/register", json={"email": "test@example.com", "password": "senha123"})
        assert register_response.status_code == 200
        data = register_response.json()
        assert "id" in data
        assert data["email"] == "test@example.com"

        # 2. Faz o login
        login_response = await ac.post("/auth/login", json={"email": "test@example.com", "password": "senha123"})
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        assert token

        # 4. Deleta o usuário criado
        delete_response = await ac.delete("/auth/user/me", headers={"Authorization": f"Bearer {token}"})
        assert delete_response.status_code == 204

@pytest.mark.asyncio
async def test_register_duplicate_email_returns_error():
    async with AsyncClient(base_url=BASE_URL) as ac:
        # 1. Registra um usuário novo
        await ac.post("/auth/register", json={"email": "testdup@example.com", "password": "senha123"})

        # 2. Tenta registrar o mesmo email de novo
        duplicate_response = await ac.post("/auth/register", json={"email": "testdup@example.com", "password": "senha123"})
        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "Email already registered"

        # 3. Faz o login
        login_response = await ac.post("/auth/login", json={"email": "testdup@example.com", "password": "senha123"})
        token = login_response.json()["access_token"]

        # 4. Deleta o usuário criado
        delete_response = await ac.delete("/auth/user/me", headers={"Authorization": f"Bearer {token}"})
        assert delete_response.status_code == 204

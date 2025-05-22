import pytest
import uuid
from httpx import AsyncClient
from app.core.config import BASE_URL

def generate_unique_email():
    return f"{uuid.uuid4()}@example.com"

@pytest.mark.asyncio
async def test_user_register_login_refresh_and_delete():
    email = generate_unique_email()
    password = "senha123"

    async with AsyncClient(base_url=BASE_URL) as ac:
        # 1. Registra o usuário
        register_response = await ac.post("/auth/register", json={"email": email, "password": password})
        assert register_response.status_code == 200
        assert register_response.json()["email"] == email

        # 2. Faz login
        login_response = await ac.post("/auth/login", json={"email": email, "password": password})
        assert login_response.status_code == 200
        tokens = login_response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        assert access_token and refresh_token

        # 3. Faz refresh do token
        refresh_response = await ac.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert refresh_response.status_code == 200
        refreshed_tokens = refresh_response.json()
        assert "access_token" in refreshed_tokens
        assert "refresh_token" in refreshed_tokens

        # 4. Acessa rota protegida ou deleta
        delete_response = await ac.delete("/auth/user/me", headers={"Authorization": f"Bearer {access_token}"})
        assert delete_response.status_code == 204

@pytest.mark.asyncio
async def test_register_duplicate_email_returns_error():
    email = generate_unique_email()
    password = "senha123"

    async with AsyncClient(base_url=BASE_URL) as ac:
        # 1. Registra usuário
        await ac.post("/auth/register", json={"email": email, "password": password})

        # 2. Tenta registrar o mesmo email
        duplicate_response = await ac.post("/auth/register", json={"email": email, "password": password})
        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "Email already registered"

        # 3. Login e delete
        login_response = await ac.post("/auth/login", json={"email": email, "password": password})
        token = login_response.json()["access_token"]
        delete_response = await ac.delete("/auth/user/me", headers={"Authorization": f"Bearer {token}"})
        assert delete_response.status_code == 204

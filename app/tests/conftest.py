import os
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.database import Base, get_db
from app.models import User, Client
from app.core.security import hash_password
from app.utils.jwt import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Remove arquivo se existir para garantir banco limpo
if os.path.exists("test.db"):
    os.remove("test.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    admin_user = User(
        email="admin@test.com",
        hashed_password=hash_password("admin123"),
        is_admin=1,
        is_active=1,
    )
    regular_user = User(
        email="user@test.com",
        hashed_password=hash_password("user123"),
        is_admin=0,
        is_active=1,
    )
    db.add_all([admin_user, regular_user])
    db.commit()
    db.close()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def token_admin():
    return create_access_token({"sub": "admin@test.com", "is_admin": True})


@pytest.fixture()
def token_user():
    return create_access_token({"sub": "user@test.com", "is_admin": False})


@pytest.fixture()
def create_test_client():
    db = TestingSessionLocal()
    unique_email = f"{uuid.uuid4()}@test.com"
    client = Client(
        name="Test Client",
        email=unique_email,
        cpf=str(uuid.uuid4().int)[:11],
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    db.close()
    return client

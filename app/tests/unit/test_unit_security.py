from app.core.security import hash_password


def test_hash_password_produces_different_output():
    password = "senha123"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)

    # Mesmo input, outputs diferentes
    assert hashed1 != hashed2
    assert hashed1.startswith("$2b$")

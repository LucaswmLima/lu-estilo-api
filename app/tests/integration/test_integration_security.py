from app.core.security import hash_password, verify_password


def test_hash_and_verify_password():
    password = "minha_senha_segura"

    # Gera o hash da senha
    hashed = hash_password(password)

    # O hash não deve ser igual à senha original
    assert hashed != password
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")

    # Verifica que a senha bate com o hash
    assert verify_password(password, hashed)

    # Verifica que uma senha errada não bate
    assert not verify_password("senha_errada", hashed)

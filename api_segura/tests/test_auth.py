# tests/test_auth.py

import uuid

def test_register_user(client):
    unique_email = f"test_{uuid.uuid4().hex}@example.com"
    response = client.post("/auth/register", json={
        "username": "teste",
        "email": unique_email,
        "password": "123456"
    })

    assert response.status_code == 201
    assert response.get_json()["message"] == "Utilizador registado com sucesso"

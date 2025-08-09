import json

def test_register_user(client):
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "user"
    })
    assert response.status_code == 201
    assert "id" in response.get_json()

def test_login_user(client):
    # First register the user
    client.post("/auth/register", json={
        "name": "Login User",
        "email": "login@example.com",
        "password": "password123",
        "role": "user"
    })

    # Then login
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

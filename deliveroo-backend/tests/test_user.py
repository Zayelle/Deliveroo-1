def register_and_login(client):
    client.post("/auth/register", json={
        "name": "User A",
        "email": "usera@example.com",
        "password": "password123",
        "role": "user"
    })
    res = client.post("/auth/login", json={
        "email": "usera@example.com",
        "password": "password123"
    })
    return res.get_json()["access_token"]

def test_get_profile(client):
    token = register_and_login(client)

    res = client.get("/profile", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    assert "email" in res.get_json()

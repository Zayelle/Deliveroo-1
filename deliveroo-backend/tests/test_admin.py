def get_admin_token(client):
    client.post("/auth/register", json={
        "name": "Admin",
        "email": "admin@example.com",
        "password": "adminpass",
        "role": "admin"
    })
    res = client.post("/auth/login", json={
        "email": "admin@example.com",
        "password": "adminpass"
    })
    return res.get_json()["access_token"]

def test_get_all_users_admin(client):
    token = get_admin_token(client)

    res = client.get("/admin/users", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

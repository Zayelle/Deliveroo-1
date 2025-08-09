import json

def get_auth_token(client):
    client.post("/auth/register", json={
        "name": "Parcel Tester",
        "email": "parcel@example.com",
        "password": "pass123",
        "role": "user"
    })
    res = client.post("/auth/login", json={
        "email": "parcel@example.com",
        "password": "pass123"
    })
    return res.get_json()["access_token"]

def test_create_parcel(client):
    token = get_auth_token(client)

    # Seed fake locations and statuses if required
    from app.models.location import Location
    from app.models.status import Status
    from app import db

    loc1 = Location(city="Nairobi", address="Avenue 1")
    loc2 = Location(city="Mombasa", address="Avenue 2")
    status = Status(name="Pending")
    db.session.add_all([loc1, loc2, status])
    db.session.commit()

    response = client.post("/parcels", json={
        "description": "Books",
        "origin_id": loc1.id,
        "destination_id": loc2.id,
        "status_id": status.id
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    data = response.get_json()
    assert data["description"] == "Books"

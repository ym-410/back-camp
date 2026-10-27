from app import app

def test_create_room(test_db):
    client = app.test_client()

    response = client.post(
        "/rooms",
        json={
            "name": "Room 202",
            "capacity": 40,
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Room 202"
    assert data["capacity"] == 40
    assert "id" in data
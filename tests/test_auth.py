from app import app

def test_register(test_db):
    client = app.test_client()

    response = client.post(
        "/register",
        json = {
            "email": "newuser@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["email"] == "newuser@example.com"
    assert "id" in data
from app import app

def test_create_reservation_without_login():
    client = app.test_client()

    response = client.post(
            "/reservations",
            json = {
                "room_id": 1,
                "start_time": "2026-10-06 10:00",
                "end_time": "2026-10-06 11:00",
            },
    )

    assert response.status_code == 401
    assert response.get_json() == {"error": "unauthorized"}
            

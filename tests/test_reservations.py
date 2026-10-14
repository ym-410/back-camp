from app import app

def test_create_reservation_without_login(test_db):
    client = app.test_client() # テスト用クライアント

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


def test_create_reservations(test_db):
    client = app.test_client()

    with client.session_transaction() as sess: # テストクライアントのsessionに直接入れる
        sess["user_id"] = 1

    response = client.post(
            "/reservations",
            json = {
                "room_id": 1,
                "start_time": "2026-10-06 10:00",
                "end_time": "2026-10-06 11:00",
            },
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["user_id"] == 1
    assert data["room_id"] == 1
    assert data["start_time"] == "2026-10-06 10:00"
    assert data["end_time"] == "2026-10-06 11:00"


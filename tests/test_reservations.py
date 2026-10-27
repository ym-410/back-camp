from app import app
import sqlite3
import db

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

def test_duplicate_reservationo(test_db):
    client = app.test_client()

    with client.session_transaction() as sess:
        sess["user_id"] = 1

    first_response = client.post(
            "/reservations",
            json={
                "room_id": 1,
                "start_time": "2026-10-06 10:00",
                "end_time": "2026-10-06 11:00",
            },
    )

    second_response = client.post(
            "/reservations",
            json={
                "room_id": 1,
                "start_time": "2026-10-06 10:30",
                "end_time": "2026-10-06 11:30",
            },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.get_json() == {
            "error": "room_already_reserved"
    }

def test_delete_own_reservation(test_db):
    client = app.test_client()

    with client.session_transaction() as sess: # テストクライアントのsessionに直接入れる
        sess["user_id"] = 1

    connection = sqlite3.connect(db.DB_PATH)
    connection.execute(

        """
        INSERT INTO reservations(
            id,
            user_id,
            room_id,
            start_time,
            end_time
        )
        VALUES (?, ?, ?, ?, ?)
        """, (1, 1, 1, "2026-10-06 10:00", "2026-10-06 11:00",),
    )

    connection.commit()
    connection.close()

    response = client.delete("/reservations/1")

    assert response.status_code == 200
    assert response.get_json() == {"message": "deleted"}

    connection = sqlite3.connect(db.DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id
        FROM reservations
        WHERE id = ?
        """, (1,),
    )

    reservation = cursor.fetchone()
    connection.close()

    assert reservation is None

def test_delete_other_users_reservation(test_db):

    client = app.test_client()

    with client.session_transaction() as sess: # テストクライアントのsessionに直接入れる
        sess["user_id"] = 2

    connection = sqlite3.connect(db.DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute(
        """
        INSERT INTO reservations (
            user_id,
            room_id,
            start_time,
            end_time
        )
        VALUES(?, ?, ?, ?)
        """, (1, 1, "2026-10-06 12:00", "2026-10-06 13:00",),
    )

    reservation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    response = client.delete(
        f"/reservations/{reservation_id}"
    )

    assert response.status_code == 403
    assert response.get_json() == {"error": "forbidden"}
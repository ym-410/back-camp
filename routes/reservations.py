from flask import Blueprint, request, session
from db import get_db

reservations_bp = Blueprint("reservations", __name__)

# 予約作成
@reservations_bp.route("/reservations", methods=["POST"])
def create_reservation():
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "unauthorized"}, 401

    data = request.get_json()

    room_id = data["room_id"]

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
            """
            INSERT INTO reservations (user_id, room_id)
            VALUES (?, ?)
            """, (user_id, room_id)
    )

    reservation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
            "id": reservation_id,
            "user_id": user_id,
            "room_id": room_id
    }, 201

# 予約取得
@reservations_bp.route("/my-reservations")
def get_my_reservations():
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "unauthorized"}, 401

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
            """
            SELECT
                id,
                user_id,
                room_id
            FROM reservations
            WHERE user_id = ?
            """, (user_id,)
    )

    rows = cursor.fetchall()
    connection.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "user_id": row[1],
            "room_id": row[2]
        })

    return result, 200

# 予約1件取得し編集
@reservations_bp.route("/reservations/<int:reservation_id>", methods=["PUT"])
def update_reservation(reservation_id):
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "unauthorized"}, 401

    data = request.get_json()

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
            """
            SELECT
                id,
                user_id,
                room_id
            FROM reservations
            WHERE id = ?
            """, (reservation_id,)
    )

    reservation = cursor.fetchone()

    if reservation is None:
        connection.close()
        return {"error": "not_found"}, 404

    cursor.execute(
        """
        SELECT is_admin FROM users
        WHERE id = ?
        """, (user_id,)
    )
    user = cursor.fetchone()

    if user_id != reservation[1] and user[0] != 1:
        connection.close()
        return {"error": "forbidden"}, 403

    cursor.execute(
            """
            UPDATE reservations
            SET room_id = ?
            WHERE id = ?
            """, (data["room_id"], reservation_id)
    )

    connection.commit()
    connection.close()

    return {
            "id": reservation_id,
            "user_id": reservation[1],
            "room_id": data["room_id"]
    }, 200


# 削除
@reservations_bp.route("/reservations/<int:reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id):
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "unauthorized"}, 401

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
            """
            SELECT id, user_id
            FROM reservations
            WHERE id = ?
            """, (reservation_id,)
    )
    reservation = cursor.fetchone()

    if reservation is None:
        connection.close()
        return {"error": "reservation_not_found"}, 404

    cursor.execute(
        """
        SELECT is_admin FROM users
        WHERE id = ?
        """, (user_id,)
    )
    user = cursor.fetchone()

    if reservation[1] != user_id and user[0] != 1:
        connection.close()
        return {"error": "forbidden"}, 403

    cursor.execute(
            """
            DELETE FROM reservations
            WHERE id = ?
            """, (reservation_id,)
    )

    connection.commit()
    connection.close()

    return {"message": "deleted"}, 200

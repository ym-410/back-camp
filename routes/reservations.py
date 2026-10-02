from flask import Blueprint, request, session
from db import get_db

reservations_bp = Blueprint("reservations", __name__)

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

from flask import Blueprint, request
from db import get_db

rooms_bp = Blueprint("rooms", __name__)


# 全部屋表示
@rooms_bp.route("/rooms")
def get_rooms():
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(
            """
            SELECT * FROM rooms
            """
    )

    rows = cursor.fetchall()
    connection.close()

    result = []

    for row in rows:
        result.append({
            "id": row[0],
            "name": row[1],
            "capacity": row[2]
        })
    
    return result

# 一件表示
@rooms_bp.route("/rooms/<int:room_id>")
def get_room(room_id):
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM rooms
        WHERE id = ?
        """,
        (room_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return {"error": "room_not_found"}, 404

    room = {
        "id": row[0],
        "name": row[1],
        "capacity": row[2]
    }

    return room

# 部屋の登録
@rooms_bp.route("/rooms", methods=["POST"])
def create_room():
    if not request.is_json:
        return {"error": "json_required"}, 400

    data = request.get_json()

    # 必須項目
    if "name" not in data:
        return {"error": "name_required"}, 400

    if "capacity" not in data:
        return {"error": "capacity_required"}, 400

    # 型
    if not isinstance(data["name"], str):
        return {"error": "name_must_be_string"}, 400

    if not isinstance(data["capacity"], int):
        return {"error": "capacity_must_be_integer"}, 400

    # 値
    if data["name"].strip() == "":
        return {"error": "invalid_name"}, 400

    if data["capacity"] <= 0:
        return {"error": "invalid_capacity"}, 400

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO rooms (name, capacity)
        VALUES (?, ?)
        """,
        (data["name"], data["capacity"])
    )

    room_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": room_id,
        "name": data["name"],
        "capacity": data["capacity"]
    }, 201

# 部屋情報の編集
@rooms_bp.route("/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    data = request.get_json()

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE rooms
        SET name = ?, capacity = ?
        WHERE id = ?
        """,
        (data["name"], data["capacity"], room_id)
    )

    if cursor.rowcount == 0:
        connection.close()
        return {"error": "room_not_found"}, 404

    connection.commit()
    connection.close()

    return {
        "id": room_id,
        "name": data["name"],
        "capacity": data["capacity"]
    }

# 部屋情報の削除
@rooms_bp.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
            """DELETE FROM rooms
            WHERE id = ?
            """, (room_id,)
    )

    if cursor.rowcount == 0:
        connection.close()
        return {"error": "room_not_found"}, 404

    connection.commit()
    connection.close()

    return {"message": "deleted"}, 200

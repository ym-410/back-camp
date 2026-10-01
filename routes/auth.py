from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

auth_bp = Blueprint("auth", __name__)

# user情報登録
@auth_bp.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return {"error": "json_required"}, 400

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    password_hash = generate_password_hash(password)

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES(?, ?)
            """, (email, password_hash)
    )

    user_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return {
            "id": user_id,
            "email": email
    }, 201

# 認証
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    connection = get_db()
    cursor = connection.cursor()
    
    cursor.execute(
            """
            SELECT
                id,
                email,
                password_hash
            FROM users
            WHERE email = ?
            """, (email,)
    )

    user = cursor.fetchone()
    connection.close()

    if user is None:
        return {"error": "invalid_credentials"}, 401

    if not check_password_hash(user[2], password):
        return {"error": "invalid_credentials"}, 401

    session["user_id"] = user[0]

    return {
            "id": user[0],
            "email": user[1]
    }, 200

@auth_bp.route("/me")
def me():
    user_id = session.get("user_id")

    if user_id is None:
        return {"error": "unauthorizzed"}, 401

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute(
            """
            SELECT
                id,
                email
            FROM users
            WHERE id = ?
            """, (user_id,)
    )

    user = cursor.fetchone()
    connection.close()

    if user is None:
        return {"error": "unauthorized"}, 401

    return {
            "id": user[0],
            "email": user[1]
    }, 200

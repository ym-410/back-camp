import os
import sqlite3
import pytest
import db


TEST_DB = "test.db"


@pytest.fixture # テスト用の準備処理
def test_db():
    db.DB_PATH = TEST_DB

    connection = sqlite3.connect(TEST_DB)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE rooms (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            capacity INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE reservations (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            start_time TEXT,
            end_time TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
        """
    )

    cursor.execute(
        """
        INSERT INTO users(
            id,
            email,
            password_hash,
            is_admin
        )
        VALUES (?, ?, ?, ?)
        """, (1, "test@example.com", "dummy_hash", 0)
    )

    cursor.execute(
        """
        INSERT INTO users(
            id,
            email,
            password_hash,
            is_admin
        )
        VALUES(?, ?, ?, ?)
        """, (2, "other@example.com", "dummy_hash", 0)
    )

    cursor.execute(
        """
        INSERT INTO rooms(
            id,
            name,
            capacity
        )
        VALUES (?, ?, ?)
        """, (1, "Room 101", 30)
    )

    connection.commit()
    connection.close()

    yield # テスト前後の境界線

    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

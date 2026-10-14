import sqlite3

DB_PATH = "app.db"

def get_db():
    return sqlite3.connect(DB_PATH)

import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "data" / "books.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    # SQLite cần bật kiểm tra khóa ngoại trên từng kết nối.
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

from contextlib import closing

import database


def init_db():
    database.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(database.get_connection()) as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT
            );

            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                price REAL NOT NULL CHECK (price >= 0),
                quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
            );
        """)


if __name__ == "__main__":
    init_db()
    print(database.DATABASE_PATH)

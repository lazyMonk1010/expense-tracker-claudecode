import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    from werkzeug.security import generate_password_hash
    conn = get_db()
    users = [
        ("Priya Sharma", "priya@example.com", generate_password_hash("password123")),
        ("Rahul Verma",  "rahul@example.com",  generate_password_hash("password123")),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        users,
    )
    conn.commit()

    user_id = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("priya@example.com",)
    ).fetchone()["id"]

    expenses = [
        (user_id, 4500.0, "Bills",     "2026-05-01", "Electricity bill"),
        (user_id,  850.0, "Food",      "2026-05-03", "Groceries"),
        (user_id,  320.0, "Transport", "2026-05-05", "Cab to office"),
        (user_id, 1200.0, "Health",    "2026-05-10", "Pharmacy"),
        (user_id,  600.0, "Food",      "2026-05-15", "Restaurant"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()

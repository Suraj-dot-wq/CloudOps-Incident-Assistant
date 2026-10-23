import sqlite3
from datetime import datetime, timezone

DB_PATH = "/data/incidents.db"


def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10)


def initialize_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                severity TEXT NOT NULL,
                title TEXT NOT NULL,
                observed_value TEXT NOT NULL,
                recommendation TEXT NOT NULL
            )
        """)


def record_incidents(incidents):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with get_connection() as conn:
        for incident in incidents:
            conn.execute("""
                INSERT INTO incidents
                (created_at, severity, title, observed_value, recommendation)
                VALUES (?, ?, ?, ?, ?)
            """, (
                now,
                incident["severity"],
                incident["title"],
                incident["value"],
                incident["action"]
            ))


def get_recent_incidents(limit=50):
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, created_at, severity, title, observed_value, recommendation
            FROM incidents
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()


def clear_incidents():
    with get_connection() as conn:
        conn.execute("DELETE FROM incidents")

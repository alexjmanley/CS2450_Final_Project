import sqlite3
from typing import List, Dict, Optional

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    start TEXT NOT NULL,
    end TEXT,
    description TEXT
);
"""


def init_db(db_path: str) -> sqlite3.Connection:
    """Initialize the SQLite database and return a connection."""
    conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()
    return conn


def add_event(conn: sqlite3.Connection, title: str, start: str, end: Optional[str] = None, description: Optional[str] = None) -> int:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO events (title, start, end, description) VALUES (?, ?, ?, ?)",
        (title, start, end, description),
    )
    conn.commit()
    return cur.lastrowid


def list_events(conn: sqlite3.Connection, date: Optional[str] = None) -> List[Dict]:
    cur = conn.cursor()
    if date:
        # Find events where start begins with date (assumes ISO date prefix)
        cur.execute("SELECT id, title, start, end, description FROM events WHERE start LIKE ? ORDER BY start", (f"{date}%",))
    else:
        cur.execute("SELECT id, title, start, end, description FROM events ORDER BY start")
    rows = cur.fetchall()
    return [
        {"id": r[0], "title": r[1], "start": r[2], "end": r[3], "description": r[4]} for r in rows
    ]


def remove_event(conn: sqlite3.Connection, event_id: int) -> bool:
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    return cur.rowcount > 0

from typing import Optional, List, Dict
import sqlite3
from dateutil import parser as dateparser

from .db import init_db, add_event as db_add_event, list_events as db_list_events, remove_event as db_remove_event


class Calendar:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = init_db(db_path)

    def add_event(self, title: str, start: str, end: Optional[str] = None, description: Optional[str] = None) -> int:
        # Normalize datetimes to ISO strings
        start_iso = self._to_iso(start)
        end_iso = self._to_iso(end) if end else None
        return db_add_event(self.conn, title, start_iso, end_iso, description)

    def list_events(self, date: Optional[str] = None) -> List[Dict]:
        # if date provided, expect YYYY-MM-DD or parseable and pass prefix
        if date:
            d = self._to_date_str(date)
            return db_list_events(self.conn, d)
        return db_list_events(self.conn, None)

    def remove_event(self, event_id: int) -> bool:
        return db_remove_event(self.conn, event_id)

    def _to_iso(self, text: str) -> str:
        dt = dateparser.parse(text)
        return dt.isoformat()

    def _to_date_str(self, text: str) -> str:
        d = dateparser.parse(text).date()
        return d.isoformat()

import sqlite3
import json
from engine.core.event import VisionEvent


class SQLiteEventStore:
    def __init__(self, db_path="data/events.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event_type TEXT,
            confidence REAL,
            metadata TEXT
        )
        """)
        self.conn.commit()

    def save(self, event: VisionEvent):
        self.conn.execute(
            """
            INSERT INTO events (timestamp, event_type, confidence, metadata)
            VALUES (?, ?, ?, ?)
            """,
            (
                event.timestamp.isoformat(),
                event.event_type,
                event.confidence,
                json.dumps(event.metadata)
            )
        )
        self.conn.commit()

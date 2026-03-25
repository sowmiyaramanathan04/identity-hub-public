import sqlite3
from pathlib import Path
import time

DB_PATH = Path(__file__).parent / "public.db"

def init_public_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS access_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        duid TEXT,
        service TEXT,
        decision TEXT,
        metadata_hash TEXT,
        timestamp INTEGER
    )
    """)

    conn.commit()
    conn.close()

def log_access(duid, service, decision, metadata_hash):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO access_logs (duid, service, decision, metadata_hash, timestamp) VALUES (?, ?, ?, ?, ?)",
        (duid, service, decision, metadata_hash, int(time.time()))
    )

    conn.commit()
    conn.close()

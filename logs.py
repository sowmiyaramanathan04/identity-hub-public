import sqlite3
from pathlib import Path
import time
from datetime import datetime
import os

DB_PATH = os.path.join("/tmp", "public.db")


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

    timestamp = int(time.time())

    cur.execute(
        "INSERT INTO access_logs (duid, service, decision, metadata_hash, timestamp) VALUES (?, ?, ?, ?, ?)",
        (duid, service, decision, metadata_hash, timestamp)
    )

    conn.commit()
    conn.close()

    # 🔥 Demo-friendly log
    readable_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    print(f"""
    ===== ACCESS LOG =====
    Time     : {readable_time}
    DUID     : {duid}
    Service  : {service}
    Decision : {decision}
    ======================
    """)
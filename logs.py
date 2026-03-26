from datetime import datetime

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

    
    readable_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    print(f"""
    ===== ACCESS LOG =====
    Time     : {readable_time}
    DUID     : {duid}
    Service  : {service}
    Decision : {decision}
    Device   : {metadata_hash[:10]}...
    ======================
    """)
import sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_PATH = BASE_DIR / "data/logs/search_logs.db"


def init_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
CREATE TABLE IF NOT EXISTS search_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    top_k INTEGER,
    alpha REAL,
    latency_ms REAL,
    result_count INTEGER,
    zero_result INTEGER,
    timestamp TEXT
)
""")

    conn.commit()
    conn.close()


def log_search(query, top_k, alpha, latency, result_count):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    zero_result = 1 if result_count == 0 else 0

    cursor.execute("""
    INSERT INTO search_logs
    (query, top_k, alpha, latency_ms, result_count, zero_result, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        query,
        top_k,
        alpha,
        latency,
        result_count,
        zero_result,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_metrics():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM search_logs")
    total_requests = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(latency_ms) FROM search_logs")
    avg_latency = cursor.fetchone()[0]

    cursor.execute("""
SELECT query, COUNT(*)
FROM search_logs
WHERE zero_result = 1
GROUP BY query
ORDER BY COUNT(*) DESC
LIMIT 5
""")

    zero_result_queries = cursor.fetchall()

    top_queries = cursor.fetchall()

    conn.close()

    return {
    "total_requests": total_requests,
    "avg_latency": avg_latency or 0,
    "top_queries": top_queries,
    "zero_result_queries": zero_result_queries
}

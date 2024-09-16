import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('sheet_changes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS changes
                 (timestamp TEXT, change_type TEXT, row_number INTEGER, old_value TEXT, new_value TEXT)''')
    conn.commit()
    return conn

def log_changes_to_db(conn, changes):
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    for change in changes:
        c.execute("INSERT INTO changes VALUES (?, ?, ?, ?, ?)",
                  (timestamp, change['type'], change['row'], change['old'], change['new']))
    conn.commit()

def get_recent_changes(conn, limit=10):
    c = conn.cursor()
    c.execute("SELECT * FROM changes ORDER BY timestamp DESC LIMIT ?", (limit,))
    return c.fetchall()
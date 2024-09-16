import mysql.connector
from datetime import datetime

def init_db():
  conn = mysql.connector.connect(
      host="localhost",
      user="root",
      password="pes2ug21cs556",
      database="Superjoin"
  )
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS changes
               (id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp VARCHAR(255),
                change_type VARCHAR(255),
                row_num INT,
                old_value TEXT,
                new_value TEXT)''')
  conn.commit()
  return conn

def log_changes_to_db(conn, log_file):
  c = conn.cursor()
  
  with open(log_file, 'r') as f:
      lines = f.readlines()
  
  current_timestamp = None
  change_type = None
  for line in lines:
      line = line.strip()
      if line.startswith("Timestamp:"):
          current_timestamp = line.split("Timestamp: ")[1]
      elif line.startswith("Initial data load:"):
          change_type = "initial_load"
      elif line.startswith("New row"):
          try:
              parts = line.split(":", 1)
              row_number = int(parts[0].split()[2])
              new_value = parts[1].strip() if len(parts) > 1 else ""
              c.execute("INSERT INTO changes (timestamp, change_type, row_num, old_value, new_value) VALUES (%s, %s, %s, %s, %s)",
                        (current_timestamp, change_type or "new_row", row_number, "", new_value))
          except ValueError as e:
              print(f"Error processing line: {line}")
              print(f"Error details: {e}")
      elif line.startswith("Row"):
          try:
              parts = line.split(":", 1)
              row_number = int(parts[0].split()[1])
              old_value, new_value = parts[1].strip().split(" -> ")
              c.execute("INSERT INTO changes (timestamp, change_type, row_num, old_value, new_value) VALUES (%s, %s, %s, %s, %s)",
                        (current_timestamp, "row_changed", row_number, old_value, new_value))
          except ValueError as e:
              print(f"Error processing line: {line}")
              print(f"Error details: {e}")
  
  conn.commit()

def get_recent_changes(conn, limit=10):
  c = conn.cursor()
  c.execute("SELECT * FROM changes ORDER BY id DESC LIMIT %s", (limit,))
  return c.fetchall()
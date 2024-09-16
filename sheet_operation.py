from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import json


def get_sheet_data(creds, spreadsheet_id, range_name):
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result.get("values", [])
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

def compare_and_log_changes(new_data, log_file, state_file):
  timestamp = datetime.now().isoformat()
  
  try:
      with open(state_file, 'r') as f:
          content = f.read().strip()
          old_data = json.loads(content) if content else None
  except (FileNotFoundError, json.JSONDecodeError):
      old_data = None

  changes = []

  with open(log_file, 'a') as f:
      f.write(f"Timestamp: {timestamp}\n")
      
      if not old_data:
          f.write("Initial data load:\n")
          for i, row in enumerate(new_data):
              f.write(f"New row {i+1}: {','.join(row)}\n")
              changes.append({"type": "new_row", "row": i+1, "data": row})
      else:
          for i, (old_row, new_row) in enumerate(zip(old_data, new_data)):
              if old_row != new_row:
                  f.write(f"Row {i+1} changed: {','.join(old_row)} -> {','.join(new_row)}\n")
                  changes.append({"type": "row_changed", "row": i+1, "old": old_row, "new": new_row})
                  
                  # Log cell-level changes
                  for j, (old_cell, new_cell) in enumerate(zip(old_row, new_row)):
                      if old_cell != new_cell:
                          f.write(f"  Cell {i+1},{j+1} changed: {old_cell} -> {new_cell}\n")
          
          if len(new_data) > len(old_data):
              for i, row in enumerate(new_data[len(old_data):], start=len(old_data)):
                  f.write(f"New row added: {','.join(row)}\n")
                  changes.append({"type": "new_row", "row": i+1, "data": row})
          elif len(new_data) < len(old_data):
              f.write(f"Rows deleted. Old row count: {len(old_data)}, New row count: {len(new_data)}\n")
              changes.append({"type": "rows_deleted", "old_count": len(old_data), "new_count": len(new_data)})
      
      f.write("\n")  # Add a blank line for readability between log entries

  # Save the new state
  with open(state_file, 'w') as f:
      json.dump(new_data, f)

  return changes

def get_change_history(log_file, limit=10):
    history = []
    with open(log_file, 'r') as f:
        lines = f.readlines()
        
    current_entry = None
    for line in reversed(lines):
        if line.startswith("Timestamp:"):
            if current_entry:
                history.append(current_entry)
                if len(history) >= limit:
                    break
            current_entry = {"timestamp": line.split(": ")[1].strip(), "changes": []}
        elif current_entry is not None:
            current_entry["changes"].append(line.strip())

    if current_entry and len(history) < limit:
        history.append(current_entry)

    return history
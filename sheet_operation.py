from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_sheet_data(creds, spreadsheet_id, range_name):
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result.get("values", [])
    except HttpError as err:
        print(f"An error occurred: {err}")
        return None

def compare_and_log_changes(old_data, new_data, log_file):
    with open(log_file, 'a') as f:
        if not old_data:
            f.write("Initial data load:\n")
            for row in new_data:
                f.write(f"New row: {','.join(row)}\n")
            return

        for i, (old_row, new_row) in enumerate(zip(old_data, new_data)):
            if old_row != new_row:
                f.write(f"Row {i+1} changed: {','.join(old_row)} -> {','.join(new_row)}\n")
        
        if len(new_data) > len(old_data):
            for row in new_data[len(old_data):]:
                f.write(f"New row added: {','.join(row)}\n")
        elif len(new_data) < len(old_data):
            f.write(f"Rows deleted. Old row count: {len(old_data)}, New row count: {len(new_data)}\n")
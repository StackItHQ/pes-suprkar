from google_sheets_handler import create_token
from sheet_operation import get_sheet_data

SPREADSHEET_ID = "1siFl1KDDVH0LKL_FIhzQIgA-X-UbGa4qItO-eMSk5rA"
RANGE_NAME = "Sheet1!A1:E"
PREVIOUS_DATA_FILE = "previous_data.json"


def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
def main():
    creds = create_token()
    if not creds:
        print("Failed to create token")
        return 

    try:
        current_data = get_sheet_data(creds, SPREADSHEET_ID, RANGE_NAME)
        if not current_data:
            print("No data found.")
            return

        print("Data successfully fetched:")
        for row in current_data:
            print(row)

    except Exception as e:
        print(f"An error occurred: {e}")
int("Data successfully fetched from Google Sheet.")

        # Load previous data
        previous_data = load_data(PREVIOUS_DATA_FILE)

        # Check if it's the first run
        is_first_run = previous_data is None

        if is_first_run:
            print("This is the first run. Initializing with current data.")
            save_data(current_data, PREVIOUS_DATA_FILE)
            
            # Log initial data to database
            initial_changes = [{"type": "initial_load", "row": i+1, "old": "", "new": ",".join(row)} for i, row in enumerate(current_data)]
            log_changes_to_db(conn, initial_changes)
            
            print("Initial data has been saved and logged.")
        else:
            # Compare and log changes
            compare_and_log_changes(previous_data, current_data, LOG_FILE)

            # Prepare changes for database
            changes = []
            with open(LOG_FILE, 'r') as f:
                for line in f:
                    if line.startswith("Row"):
                        parts = line.strip().split(': ')
                        row_num = int(parts[0].split()[1])
                        old, new = parts[1].split(' -> ')
                        changes.append({"type": "row_changed", "row": row_num, "old": old, "new": new})
                    elif line.startswith("New row added"):
                        new = line.strip().split(': ')[1]
                        changes.append({"type": "new_row", "row": len(previous_data) + 1, "old": "", "new": new})
                    elif line.startswith("Rows deleted"):
                        old, new = line.strip().split('. ')[1].split(', ')
                        changes.append({"type": "rows_deleted", "row": 0, "old": old.split(': ')[1], "new": new.split(': ')[1]})

            # Log changes to database
            log_changes_to_db(conn, changes)

            # Save current data for next comparison
            save_data(current_data, PREVIOUS_DATA_FILE)

        # Get and print recent changes
        recent_changes = get_recent_changes(conn)
        print("\nRecent changes:")
        for change in recent_changes:
            print(change)

        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
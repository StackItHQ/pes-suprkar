from google_sheets_handler import create_token
from sheet_operation import get_sheet_data, compare_and_log_changes, get_change_history
from database_operations import init_db, log_changes_to_db, get_recent_changes

SPREADSHEET_ID = "1siFl1KDDVH0LKL_FIhzQIgA-X-UbGa4qItO-eMSk5rA"
RANGE_NAME = "Sheet1!A1:E"
LOG_FILE = "sheet_changes.log"
STATE_FILE = "sheet_state.json"

def main():
    creds = create_token()
    if not creds:
        print("Failed to create token")
        return 

    try:
        # Initialize database
        conn = init_db()

        current_data = get_sheet_data(creds, SPREADSHEET_ID, RANGE_NAME)
        if not current_data:
            print("No data found.")
            return

        print("Data successfully fetched.")
        
        changes = compare_and_log_changes(current_data, LOG_FILE, STATE_FILE)
        
        if changes:
            print("Changes detected:")
            for change in changes:
                print(change)
        else:
            print("No changes detected.")

        # Log changes to database
        log_changes_to_db(conn, LOG_FILE)

        print("\nRecent change history:")
        history = get_change_history(LOG_FILE, limit=5)
        for entry in history:
            print(f"Timestamp: {entry['timestamp']}")
            for change in entry['changes']:
                print(f"  {change}")
            print()

        # Get and print recent changes from database
        print("\nRecent changes from database:")
        db_changes = get_recent_changes(conn)
        for change in db_changes:
            print(change)

        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
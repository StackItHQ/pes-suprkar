from google_sheets_handler import create_token
from sheet_operation import get_sheet_data

SPREADSHEET_ID = "1siFl1KDDVH0LKL_FIhzQIgA-X-UbGa4qItO-eMSk5rA"
RANGE_NAME = "Sheet1!A1:E"

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

if __name__ == "__main__":
    main()
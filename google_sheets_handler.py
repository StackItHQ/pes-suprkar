from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

class GoogleSheetsHandler:
    def __init__(self, credentials_path, sheet_id):
        self.sheet_id = sheet_id
        self.creds = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build('sheets', 'v4', credentials=self.creds)
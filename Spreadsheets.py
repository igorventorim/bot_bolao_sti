import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle
import pandas as pd
from dotenv import load_dotenv


class Spreadsheets:

    def __init__(self, scopes=['https://www.googleapis.com/auth/spreadsheets'], id_spreadsheet=None, range='Página1!A1:AA100000'):
        self.scopes = scopes
        self.id_spreadsheet = id_spreadsheet
        self.range = range
        self.service = None
        self.pd = None
        load_dotenv()

    def create_service(self):

        CREDENTIALS_FILE = 'credentials.json'
        TOKEN_FILE = 'token.json'
        cred = None

        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, self.scopes
                )
                cred = flow.run_local_server()

            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(cred, token)

        try:
            self.service = build(
                os.getenv('API_GOOGLE_SERVICE_NAME'), os.getenv('API_GOOGLE_VERSION'), credentials=cred
            )
            print(os.getenv('API_GOOGLE_SERVICE_NAME'),
                  'service created successfully')
        except Exception as e:
            self.service = None
            print(e)

    def create_spreadsheet_with_title(self, title='Planilha sem título'):
        self.create_service()
        spreadsheet_body = {'properties': {'title': title, 'locale': 'pt_BR'}}

        request = self.service.spreadsheets().create(body=spreadsheet_body)
        response = request.execute()

        if response['spreadsheetId'] is not None:
            self.id_spreadsheet = response['spreadsheetId']
        else:
            print("Erro ao criar planilha")

    def export_data_to_sheets(self):
        if self.service is None:
            print("Service not found!")
            return

        if self.df is None:
            print("Dataframe not found!")
            return

        response_date = self.service.spreadsheets().values().update(
            spreadsheetId=self.id_spreadsheet,
            valueInputOption='RAW',
            range=self.range,
            body=dict(
                majorDimension='ROWS',
                values=self.df.T.reset_index().T.values.tolist()
            )
        ).execute()
        print('Sheet successfully Updated')

    def read_sheets(self):
        if self.service is None:
            print("Service not found!")
            return

        sheet = self.service.spreadsheets()
        result_input = sheet.values().get(spreadsheetId=self.id_spreadsheet,
                                          range=self.range).execute()
        values_input = result_input.get('values', [])

        if not values_input:
            print('No data found.')
            self.df = None
        else:
            self.df = pd.DataFrame(values_input[1:], columns=values_input[0])


if __name__ == "__main__":
    # spread_sheats.create_service('credentials.json', 'sheets', 'v4')
    # spread_sheats.read_sheets()
    # spread_sheats.df["available"][0] = 1
    # print(spread_sheats.df.head())
    # spread_sheats.export_data_to_sheets()

    planilha = Spreadsheets()
    planilha.create_spreadsheet_with_title(
        'Planilha teste Igor')
    planilha.read_sheets()

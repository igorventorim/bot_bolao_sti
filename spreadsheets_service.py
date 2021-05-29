import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
import os
import pickle
import pandas as pd
from dotenv import load_dotenv
from bot_management import BotManagement


class SpreadsheetsService:

    def __init__(self, scopes=['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/spreadsheets'], id_spreadsheet=None, range='Página1!A1:AA100000'):
        self.scopes = scopes
        self.id_spreadsheet = id_spreadsheet
        self.range = range
        self.service = None
        self.pd = None
        load_dotenv()
        self.__create_service()

    def get_service(self):
        return self.service

    def __create_service(self):

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
        spreadsheet_body = {'properties': {'title': title, 'locale': 'pt_BR'}}

        request = self.service.spreadsheets().create(body=spreadsheet_body)
        response = request.execute()

        if response['spreadsheetId'] is not None:
            self.id_spreadsheet = response['spreadsheetId']
        else:
            print("Erro ao criar planilha")

        return response

    def add_sheet_with_name(self, tab_name):
        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": tab_name,
                            "gridProperties": {
                                "rowCount": 20,
                                "columnCount": 12
                            },
                            "tabColor": {
                                "red": 1.0,
                                "green": 1.0,
                                "blue": 1.0
                            }
                        }
                    }
                }
            ]
        }

        request = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.id_spreadsheet, body=batch_update_spreadsheet_request_body)
        response = request.execute()

        if response['spreadsheetId'] is not None:
            self.id_spreadsheet = response['spreadsheetId']
        else:
            print("Erro ao adicionar nova tab")

    def get_metadata_spreadsheet(self):
        request = self.service.spreadsheets().get(spreadsheetId=self.id_spreadsheet)
        response = request.execute()
        # TODO CATCH ERROR
        return response

    def get_sheets_properties(self):
        metadata_spreadsheet = self.get_metadata_spreadsheet()
        # TODO CATCH ERROR
        return metadata_spreadsheet['sheets']

    def delete_first_tab(self):
        self.delete_sheet_by_sheet_id(0)

    def delete_sheet_by_sheet_id(self, id):
        batch_update_spreadsheet_request_body = {
            "requests": [
                {
                    "deleteSheet": {
                        "sheetId": id
                    }
                }
            ]
        }
        request = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.id_spreadsheet, body=batch_update_spreadsheet_request_body)
        response = request.execute()

    def delete_sheet_by_sheet_name(self, name):
        sheets_properties = self.get_sheets_properties()
        id = None
        for sheet in sheets_properties:
            if sheet['properties']['title'] == name:
                id = sheet['properties']['sheetId']

        if id is not None:
            self.delete_sheet_by_sheet_id(id)
        else:
            print('Sheet not found!')

    def export_data_to_sheets(self, range=None):
        if self.service is None:
            print("Service not found!")
            return

        if self.df is None:
            print("Dataframe not found!")
            return

        response_date = self.service.spreadsheets().values().update(
            spreadsheetId=self.id_spreadsheet,
            valueInputOption='RAW',
            range=range if range is not None else self.range,
            body=dict(
                majorDimension='ROWS',
                values=self.df.T.reset_index().T.values.tolist()
            )
        ).execute()
        print('Sheet successfully Updated')

    def read_sheets(self, range=None):
        if self.service is None:
            print("Service not found!")
            return

        sheet = self.service.spreadsheets()
        result_input = sheet.values().get(spreadsheetId=self.id_spreadsheet,
                                          range=range if range is not None else self.range).execute()
        values_input = result_input.get('values', [])

        if not values_input:
            print('No data found.')
            self.df = None
        else:
            self.df = pd.DataFrame(values_input[1:], columns=values_input[0])


if __name__ == "__main__":
    planilha = Spreadsheets(
        id_spreadsheet='1KCZnyqQUF6MoBIz89p0XWVS2wVI7tQV72K-kjQLs_hQ')
    # planilha.create_spreadsheet_with_title(
    # 'Planilha teste Igor')
    planilha.add_sheet_with_name('rodada3')
    planilha.get_metadata_spreadsheet()
    print("Número de tabs na planilha: {}".format(
        len(planilha.get_sheets_properties())))
    # planilha.read_sheets()

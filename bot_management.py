import os


class BotManagement:

    @staticmethod
    def set_config():
        BOT_MANAGEMENT_FILENAME = 'bot_management.config'

        if not os.path.isfile(BOT_MANAGEMENT_FILENAME):
            with open(BOT_MANAGEMENT_FILENAME, 'w') as file_config:
                file_config.write('chat_id;title;spreadsheet_id\n')

    def update_title(self):
        pass

    def add_bolao(self):
        pass

    def get_boloes(self):
        pass

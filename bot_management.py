import os


class BotManagement:
    BOT_MANAGEMENT_FILENAME = 'bot_management.config'

    @staticmethod
    def set_config():
        
        if not os.path.isfile(BotManagement.BOT_MANAGEMENT_FILENAME):
            with open(BotManagement.BOT_MANAGEMENT_FILENAME, 'w') as file_config:
                file_config.write('chat_id;title;spreadsheet_id\n')

    def update_title(self):
        pass

    def add_bolao(self, chat_id, title, spreadsheet_id):
        with open(BotManagement.BOT_MANAGEMENT_FILENAME, 'a') as file_config:
            file_config.write('{};{};{}\n'.format(
                chat_id, title, spreadsheet_id))

    def get_boloes(self):
        pass

    def verificar_existencia_bolao_por_chat_id(self, chat_id):

        boloes_cadastrados_dict = self.__get_dict_boloes_cadastrados_por_chatid()

        if chat_id in boloes_cadastrados_dict:
            return True
        else:
            return False

    def __get_dict_boloes_cadastrados_por_chatid(self):
        with open(BotManagement.BOT_MANAGEMENT_FILENAME, 'r') as file_config:
            boloes_cadastrados_dict = {}
            linhas = file_config.readlines()
            boloes_info_list = [ x.rstrip('\n').split(';') for x in linhas][1:]
            
            for bolao_info in boloes_info_list:
                boloes_cadastrados_dict[bolao_info[0]] = bolao_info

            return boloes_cadastrados_dict
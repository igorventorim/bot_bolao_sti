# Name of function is the command used in telegram. i.e. /start
# Create in this file just command functions

from spreadsheets_service import SpreadsheetsService
from bot_management import BotManagement
import ipdb


def start(update, context):
    update.message.reply_text(
        "Eu sou um robô, por favor, converse comigo!\nDigite /ajuda para listar os comandos disponíveis.")


def ajuda(update, context):
    update.message.reply_text(
        "Olá! Esses são os seguintes comandos disponíveis: \n\n" +
        "/start para conhecer mais sobre o robô administrador do bolão.\n" +
        "/ajuda lista os comandos disponíveis para o robô.\n" +
        "/rodada_brasileirao <numero_da_rodada_que_deseja_informacao> lista os jogos do brasileirao para a rodada desejada.\n" +
        "/rodada_bolao <numero_da_rodada_que_deseja_informacao> lista os jogos do bolão para a rodada desejada.\n"
    )


def rodada_brasileirao(update, context):
    try:
        rodada = int(context.args[0])
        if rodada < 1 or rodada > 38:
            update.message.reply_text(
                "Desculpe, rodada não encontrada. Favor confirmar se o valor da rodada está correto."
            )
            return

        from rodada_service import RodadaService

        rodadaService = RodadaService(rodada)
        update.message.reply_text(rodadaService.getJogosRodadaBrasileirao())

    except (IndexError, ValueError):
        update.message.reply_text(
            "Use: /rodada_brasileirao <numero_da_rodada_que_deseja_informacao>"
        )


def rodada_bolao(update, context):
    try:
        rodada = int(context.args[0])
        if rodada < 1 or rodada > 38:
            update.message.reply_text(
                "Desculpe, rodada não encontrada. Favor confirmar se o valor da rodada está correto."
            )
            return

        # TODO IMPLEMENTAR

    except (IndexError, ValueError):
        update.message.reply_text(
            "Use: /rodada_bolao <numero_da_rodada_que_deseja_informacao>"
        )


def palpite(update, context):
    pass


def palpites(update, context):
    pass


def ranking(update, context):
    pass


def participar(update, context):

    if update.message.chat.type in ['group', 'supergroup']:
        spreadsheets_service = SpreadsheetsService()

        if not bot_management.verificar_existencia_bolao_por_chat_id(update.message.chat.id):
            spreadsheets_metadata = spreadsheets_service.get_metadata_spreadsheet()
            update.message.reply_text('Esse grupo ainda não possui nenhum bolão ativo, peça para algum administrador do grupo iniciar o bolão')
            return
        
        #TODO VERIFICAR SE PARTICIPANTE JÁ NÃO SE ENCONTRA INSCRITO
        #TODO INSCREVER PARTICIPANTE

        update.message.reply_text(
            '{} inscrito com sucesso.'.format(update.message.full_name))
    else:
        update.message.reply_text(
            'Só é possível se inscrever em um bolão a partir de um grupo.')


def iniciar(update, context):
    spreadsheets_service = SpreadsheetsService()
    bot_management = BotManagement()
    if not update.message.chat.type in ['group', 'supergroup']:
        update.message.reply_text(
            'Esse comando só é permitido a partir de um grupo.')
        return
    
    if not update.message.chat.get_member(update.message.from_user.id).status in ['creator', 'administrator']:
        update.message.reply_text(
            'Somente administradores de grupo podem iniciar um bolão.')
        return

    if bot_management.verificar_existencia_bolao_por_chat_id(update.message.chat.id):
        spreadsheets_metadata = spreadsheets_service.get_metadata_spreadsheet()
        update.message.reply_text(
            'Esse grupo já possui um bolão ativo. Confira a planilha a seguir: ' + spreadsheets_metadata['spreadsheetUrl'])
        return

    result_criar_planilha = spreadsheets_service.create_spreadsheet_with_title(
        'bolao_' + str(update.message.chat.title))

    spreadsheets_service.add_sheet_with_name('PARTICIPANTES')
    spreadsheets_service.add_sheet_with_name('RANKING')
    spreadsheets_service.add_sheet_with_name('RODADA_1')
    spreadsheets_service.delete_first_tab()

    bot_management.add_bolao(
        update.message.chat.id, update.message.chat.title, spreadsheets_service.id_spreadsheet)

    update.message.reply_text(
        "Seu bolão foi criado! Confira a planilha a seguir: " +
        result_criar_planilha['spreadsheetUrl']
    )

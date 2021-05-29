# Name of function is the command used in telegram. i.e. /start
# Create in this file just command functions
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
    import ipdb
    ipdb.set_trace()
    pass


def palpites(update, context):
    pass


def ranking(update, context):
    pass


def participar(update, context):

    if update.message.chat.type in ['group', 'supergroup']:
        update.message.id

        update.message.reply_text(
            '{} inscrito com sucesso.'.format(update.message.full_name))
    else:
        update.message.reply_text(
            'Só é possível se inscrever em um bolão a partir de um grupo.')


def iniciar(update, context):
    # VERIFICAR SE É ADMINISTRADOR
    # VINCULAR GRUPO COM CHAT_ID e TITLE NO ARQUIVO DE GERENCIAMENTO
    # CRIAR TABELA DO BOLÃO COM TABS:[PARTICIPANTES,RANKING,RODADA_1] E VINCULAR SPREADSHEET_ID NA TABELA DE GERENCIAMENTO
    pass

# Name of function is the command used in telegram. i.e. /start
# Create in this file just command functions

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Eu sou um robô, por favor, converse comigo!\nDigite /ajuda para listar os comandos disponíveis.")


def ajuda(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Olá! Esses são os seguintes comandos cadastrados:\n" +
        "/start para conhecer mais sobre o robô administrador do bolão\n" +
        "/ajuda lista os comandos disponíveis para o robô" +
        "/rodada_brasileirao <numero_da_rodada_que_deseja_informacao>")


def rodada_brasileirao(update, context):
    try:
        rodada = int(context.args[0])
        if rodada < 1 or rodada > 38:
            update.message.reply_text(
                "Desculpe, rodada não encontrada. Favor confirmar se o valor da rodada está correto.")
            return

        from rodada_service import RodadaService

        rodadaService = RodadaService(rodada)
        update.message.reply_text(rodadaService.getJogosRodadaBrasileirao())

    except (IndexError, ValueError):
        update.message.reply_text(
            "Use: /rodada_brasileirao <numero_da_rodada_que_deseja_informacao>")


def rodada_bolao(update, context):
    try:
        rodada = int(context.args[0])
        if rodada < 1 or rodada > 38:
            update.message.reply_text(
                "Desculpe, rodada não encontrada. Favor confirmar se o valor da rodada está correto.")
            return

        # TODO IMPLEMENTAR

    except (IndexError, ValueError):
        update.message.reply_text(
            "Use: /rodada_bolao <numero_da_rodada_que_deseja_informacao>")
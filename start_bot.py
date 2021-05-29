#! /usr/bin/env python

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)
import logging
from dotenv import load_dotenv
import os
from inspect import getmembers, isfunction
import commands
from bot_management import BotManagement


def unknown(update, context):
    update.message.reply_text("Desculpe, eu não entendi esse comando.")


def error(update, context):
    print(f"Update {update} caused error {context.error}")
    update.message.reply_text("Desculpe, ocorreu um erro, procure o Danilo!")


def main() -> None:

    # Load environments variables
    load_dotenv()

    BotManagement.set_config()

    # Create the Updater and pass it your bot's token.
    updater = Updater(
        token=os.getenv('BOT_TOKEN'))

    # Add logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # add commands handler from commands.py
    commands_list = getmembers(commands, isfunction)
    for (x, y) in commands_list:
        dispatcher.add_handler(CommandHandler(x, y))

    # add message handler
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # add handler error
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    updater.idle()


if __name__ == '__main__':
    main()

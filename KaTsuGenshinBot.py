#!/usr/bin/env python3
# coding=utf-8
import os
from requests.api import delete
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from Command import *
from dotenv import load_dotenv

load_dotenv()

# Main
def main():
    
    updater = Updater( os.getenv("TELEGRAM_TOKEN") )

    updater.dispatcher.add_handler(CommandHandler('start', startbot))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('set', add))
    updater.dispatcher.add_handler(CommandHandler('add', add))
    updater.dispatcher.add_handler(CommandHandler('list', list))
    updater.dispatcher.add_handler(CommandHandler('get', finding))
    updater.dispatcher.add_handler(CommandHandler('find', finding))
    updater.dispatcher.add_handler(CommandHandler('del', delete))
    updater.dispatcher.add_handler(CommandHandler('delete', delete))
    updater.dispatcher.add_handler(CommandHandler('select', select))
    updater.dispatcher.add_handler(CommandHandler('cal', select))
    updater.dispatcher.add_handler(CommandHandler('update', setVal))

    updater.dispatcher.add_handler(CommandHandler('conch', getRandomReply))


    updater.dispatcher.add_handler(MessageHandler(Filters.text, getText))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, getPhoto))
    updater.dispatcher.add_handler(MessageHandler(Filters.document, getFile))

    

    updater.dispatcher.add_handler(CallbackQueryHandler(callback))

    print("KaTsuGenshinBot Server Running...")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


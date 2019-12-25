import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi Dear ✋ \nI'm BRS Bot ‍💻 ")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


logging.info("start")
updater.start_polling(poll_interval=1)

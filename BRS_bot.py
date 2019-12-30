import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from brs_bot import brs_parser
from brs_bot.brs_parser import pers_pos, pers_points


updater = Updater(token='', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

subjects_dict = {'ДИЯ 📔': 0, 'ДУ 📗': 1, 'МА 📕': 2, 'ОС 📙': 3, 'C 📓': 4, 'Э 📘': 6, 'ЯиМП 📒': 7}

FUNC, SUB, POS, NAME, DIS = range(5)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi Dear ✋ \nPlease, type your full name 💬 ")
    return NAME


def choose_function(update, context):
    bot = context.bot
    chat_data = context.chat_data
    chat_data['name'] = update.message.text
    keyboard = [
        [KeyboardButton('Посмотреть балл по предметам 🔍'),
         KeyboardButton('Посмотреть текущее место в рейтенге 📋')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    bot.send_message(update.message.chat_id, "Okey, what do you want❔",
                     reply_markup=reply_markup)

    return FUNC


def choose_discipline(update, context):
    bot = context.bot
    keyboard = [
        [KeyboardButton('ДИЯ 📔'),
         KeyboardButton('ДУ 📗'),
         KeyboardButton('МА 📕'),
         KeyboardButton('ОС 📙'),
         KeyboardButton('C   📓'),
         KeyboardButton('Э   📘'),
         KeyboardButton('ЯиМП 📒')],
        [KeyboardButton('All disciplines 📚')]]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    bot.send_message(update.message.chat_id, "Choose discipline 💡",
                     reply_markup=reply_markup)
    return DIS


def show_position(update, context):
    chat_data = context.chat_data
    name = chat_data['name']
    pos = pers_pos[name]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Your position is {pos}")


def cancel(update, context):
    return ConversationHandler.END


choose_category_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("start"),
                                 start)],
    states={
        NAME: [MessageHandler(Filters.text,
                                      choose_function)],

        FUNC: [MessageHandler(Filters.regex('^(Посмотреть балл по предметам 🔍)$'),
                              choose_discipline),
               MessageHandler(Filters.text,
                              show_position),

               ]
    },
    fallbacks=[MessageHandler(Filters.all, cancel)])





# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)


dispatcher.add_handler(choose_category_conversation)

logging.info("start")
updater.start_polling(poll_interval=1)


# there will be function to check your points in all subjects
# to check your position in brs
# bot will sent you new points
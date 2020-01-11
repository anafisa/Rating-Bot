import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, PicklePersistence, Updater, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from brs_bot.brs_parser import pers_pos, pers_points


my_persistence = PicklePersistence(filename='BRS_bot')

updater = Updater(token='', persistence=my_persistence, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

subjects_dict = {'ДИЯ 📔': 0, 'ДУ 📗': 1, 'МА 📕': 2, 'ОС 📙': 3, 'C   📓': 4, 'Э   📘': 6,
                 'ЯиМП 📒': 7, 'All disciplines 📚': ''}

FUNC, SUB, POS, NAME, DIS = range(5)


def start(update, context):
    chat_data = context.chat_data
    chat_data['id'] = update.message.chat.id
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Hi 👀 \nPlease, type your full name 💬 ")
    return NAME


def get_name(update, context):
    context.user_data['name'] = update.message.text
    choose_function(update, context)
    return ConversationHandler.END


def choose_function(update, context):
    bot = context.bot
    keyboard = [
        [KeyboardButton('Check up your points 🔍'),
         KeyboardButton('Check up your position 📋'),
         KeyboardButton('Subscribe to updates 👩‍💻')]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)

    bot.send_message(update.message.chat_id, "Okay, what do you want❔",
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
    return SUB


def show_position(update, context):
    name = context.user_data['name']
    pos = pers_pos[name]
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Your position is {pos}")
    choose_function(update, context)
    return ConversationHandler.END


def show_points(update, context):
    name = context.user_data['name']
    ind = subjects_dict[update.message.text]
    if ind != '':
        points = pers_points[name][ind]
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'You have {points}')
    else:
        points = pers_points[name]
        points.remove('')
        keys = list(subjects_dict.keys())[:-1]
        res = ' | '.join([keys[i] + (points[i]) for i in range(len(points))])
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=res)

    choose_function(update, context)
    return ConversationHandler.END


#def send_upd(update,context):


def cancel(update, context):
    return ConversationHandler.END


choose_category_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("start"),
                                 start),

                  MessageHandler(Filters.regex('^(Check up your points 🔍)$'),
                                 choose_discipline),

                  MessageHandler(Filters.text,
                                 show_position)
                  ],
    states={
        NAME: [MessageHandler(Filters.text,
                              get_name)],

        FUNC: [MessageHandler(Filters.regex('^(Check up your points 🔍)$'),
                              choose_discipline),

               MessageHandler(Filters.text,
                              show_position),


               # MessageHandler(Filters.text,
               #                send_upd)
               ],
        #  дописать тутъ
        SUB: [MessageHandler(Filters.text,
                             show_points),

              ]

    },

    fallbacks=[MessageHandler(Filters.all, cancel)],

    persistent=True, name='my_name')


# def callback_minute(context: telegram.ext.CallbackContext):
#     context.bot.send_message(chat_id='',
#                              text='One message every minute')
#
#
# job_minute = j.run_repeating(callback_minute, interval=60, first=0)

dispatcher.add_handler(choose_category_conversation)

logging.info("start")
updater.start_polling(poll_interval=1)

#####

####

from credentials import telegram_bot_token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup 

# Part A
token = telegram_bot_token # Replace <TOKEN> with your own token  
updater = Updater(token, use_context=True)

# Part C   InlineKeyboard
def callback(update, context):
    query=update.callback_query
    print(query.data)
    query.edit_message_text(text="Selected option: {}".format(query.data))

def handle_start_cmd(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Photo 1", callback_data='1'),
            InlineKeyboardButton("Photo 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

cmd = CommandHandler("start", handle_start_cmd)
updater.dispatcher.add_handler(cmd)
updater.dispatcher.add_handler(CallbackQueryHandler(callback))


# Part D     
def handle_help_cmd(update, context):
    update.message.reply_text('/photo <NAME OF PHOTO>')

cmd = CommandHandler('help', handle_help_cmd)
updater.dispatcher.add_handler(cmd)


# Part E     Send Photo
import requests
def handle_photo_cmd(update, context):
    update.message.reply_photo('https://media.nature.com/lw800/magazine-assets/d41586-020-01430-5/d41586-020-01430-5_17977552.jpg')
    with open(r'test.png', 'rb') as f:
        update.message.reply_photo(photo=f)


cmd = CommandHandler('photo', handle_photo_cmd)
updater.dispatcher.add_handler(cmd)


# Get Location
def handle_location_cmd(update, context):
    message = None
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message
    if message and message.location:
        current_pos = (message.location.latitude, message.location.longitude)
        print(current_pos)
        message.reply_text('Your location: ' + current_pos)
    else:
        message.reply_text('Your location is not found')

location_handler = MessageHandler(Filters.location, handle_location_cmd)
updater.dispatcher.add_handler(location_handler)


# Part F
def handle_any_msg(update, context):
    update.message.reply_text('USAGE: /start, /photo, /loc')

cmd = MessageHandler(Filters.text, handle_any_msg)
updater.dispatcher.add_handler(cmd)


# Part B
updater.start_polling()
updater.idle()

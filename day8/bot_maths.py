
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Part A
token = '1221170991:AAH3KJEdbMF0nS9UN0AuKEP4xZhp_XKZ2a0' # Replace <TOKEN> with your own token  
updater = Updater(token, use_context=True)

# Part C
def handle_start_cmd(update, context):
    update.message.reply_text('Hi, I am Mathematician!')

cmd = CommandHandler("start", handle_start_cmd)
updater.dispatcher.add_handler(cmd)

# Part D
def handle_help_cmd(update, context):
    update.message.reply_text('Type a maths equation and I will show you the answer.')

cmd = CommandHandler('help', handle_help_cmd)
updater.dispatcher.add_handler(cmd)

# Part E
def handle_maths_cmd(update, context):
    s = update.message.text
    print(s)
    exp = s.replace('/maths', '')
    try:
        result = eval(exp)
    except:
        result = 'Invalid maths expression'
    update.message.reply_text(result)

cmd = CommandHandler('maths', handle_maths_cmd)
updater.dispatcher.add_handler(cmd)

# Part F
def handle_any_msg(update, context):
    update.message.reply_text('USAGE: /maths <maths-expression>')

cmd = MessageHandler(Filters.text, handle_any_msg)
updater.dispatcher.add_handler(cmd)


# Part B
updater.start_polling()
updater.idle()

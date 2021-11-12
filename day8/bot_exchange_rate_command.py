#####
# Currency conversion using CommandHandler
# To start, create a file "credentials.py" in the same directory and add following line. Replace <TOKEN> with your own token.
#   telegram_bot_token = '<TOKEN>'
# You may also find useful bots examples at https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples
####

from credentials import telegram_bot_token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Part A
token = telegram_bot_token # Replace <TOKEN> with your own token  
updater = Updater(token, use_context=True)

# Part C
def handle_start_cmd(update, context):
    update.message.reply_text('Hi, I am Money Changer!')

cmd = CommandHandler("start", handle_start_cmd)
updater.dispatcher.add_handler(cmd)

# Part D
def handle_help_cmd(update, context):
    update.message.reply_text('Ask me about exchange rate!\nUSAGE:\n   /rate <SGD> <USD>\n   /rate <SGD> <USD,GBP>\n   /rate <SGD>')

cmd = CommandHandler('help', handle_help_cmd)
updater.dispatcher.add_handler(cmd)

# Part E
import requests
def handle_rate_cmd(update, context):
    s = update.message.text
    parts = s.split()
    base = parts[1]
    symbols = parts[2] if len(parts)>=3 else None

    URL = 'https://api.exchangeratesapi.io/latest'
    if symbols:
        params = {'symbols':symbols, 'base':base}
    else:
        params = {'base':base}
    resp = requests.get(URL, params)
    result = resp.json()

    rates = []
    for key,val in result['rates'].items():
        rates.append(f'{val} {key}')
    print(rates)

    answer = '1 {} = {}'.format(result['base'], ', '.join(rates))
    print(answer)

    update.message.reply_text(answer)

cmd = CommandHandler('rate', handle_rate_cmd)
updater.dispatcher.add_handler(cmd)

# Part F
def handle_any_msg(update, context):
    update.message.reply_text('USAGE:\n   /rate <SGD> <USD>\n   /rate <SGD> <USD,GBP>\n   /rate <SGD>')

cmd = MessageHandler(Filters.text, handle_any_msg)
updater.dispatcher.add_handler(cmd)


# Part B
updater.start_polling()
updater.idle()

#####
# Currency conversion using ConversationHandler
# To start, create a file "credentials.py" in the same directory and add following line. Replace <TOKEN> with your own token.
#   telegram_bot_token = '<TOKEN>'
# You may also find useful bots examples at https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples
####

import logging

from credentials import telegram_bot_token
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# States
BUY_SELL, TARGET_CURRENCY, TARGET_AMOUNT, BASE_CURRENCY, BASE_AMOUNT = range(5)

# Save records of all chats
records = {}

# Every new chat will start with default values
default_val = {'action': '',
               'target_currency': None,
               'target_amount': None,
               'base_currency': None,
               'base_amount': None}


def get_exchange_rate(base_currency, target_currency, action='BUY'):
    url = f'https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={target_currency}'
    import requests
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    return resp.json()


def generate_result(user_input):
    forex = get_exchange_rate(user_input['base_currency'], user_input['target_currency'])
    if not forex:
        return f"Sorry, cant get result for {user_input['base_currency']} and {user_input['target_currency']}"

    rate = forex['rates'][user_input['target_currency']]
    rate = float(rate)

    if user_input['target_amount']:
        # calculate base amount
        target_amount = float(user_input['target_amount'])
        base_amount = round(target_amount / rate, 2)
    elif user_input['base_amount']:
        base_amount = float(user_input['base_amount'])
        target_amount = round(base_amount * rate, 2)
    else:
        base_amount = 1
        target_amount = round(rate, 5)

    s = []
    s.append(user_input['action'])
    s.append(str(target_amount))
    s.append(user_input['target_currency'])
    s.append('needs' if user_input['action'] == 'BUY' else 'gets')
    s.append(str(base_amount))
    s.append(user_input['base_currency'])

    return ' '.join(s)


def start(update, context):
    global records
    user_id = update.message.from_user.id

    records[user_id] = default_val.copy()
    logger.info(f"{user_id} starts")

    # Show "Buy" and "Sell" buttons for user to click
    reply_keyboard = [['Buy', 'Sell']]
    update.message.reply_text(
        'Hi! Welcome to Money Changer. '
        'Send /cancel to stop.\n'
        'Would you like to Buy or Sell currency?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return BUY_SELL


def handle_buy_sell(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    buy_sell = update.message.text.upper()
    records[user_id]['action'] = buy_sell
    logger.info(f"{user_id}: Action = {buy_sell}")

    update.message.reply_text(f'What currency would you like to {buy_sell}',
                              reply_markup=ReplyKeyboardRemove())
    return TARGET_CURRENCY


def handle_target_currency(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    currency = update.message.text.upper()
    action = records[user_id]['action']
    records[user_id]['target_currency'] = currency
    logger.info(f'{user_id}: Target currency = {currency}')

    update.message.reply_text(f'How much {currency} would you like to {action}? \n Send /skip to skip.')

    return TARGET_AMOUNT


def handle_target_amount(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    amount = update.message.text.strip()
    records[user_id]['target_amount'] = amount
    logger.info(f'{user_id}: Target amount = {amount}')
    update.message.reply_text('What currency would you like to use?')

    return BASE_CURRENCY


def skip_target_amount(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    logger.info(f'{user_id}: Target amount = None')
    update.message.reply_text('What currency would you like to use?')

    return BASE_CURRENCY


def handle_base_currency(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    currency = update.message.text.upper()
    records[user_id]['base_currency'] = currency
    logger.info(f'{user_id}: Base currency = {currency}')

    # if target amount is provided, skip asking for base amount
    if records[user_id]['target_amount']:
        skip_base_amount(update, context)
    else:
        update.message.reply_text(f'How much {currency} would you like to use? \n Send /skip to skip.')
        return BASE_AMOUNT


def handle_base_amount(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    amount = update.message.text.strip()
    records[user_id]['base_amount'] = amount
    logger.info(f'{user_id}: Base amount = {amount}')

    # Get final result
    result = generate_result(records[user_id])
    update.message.reply_text(result)

    return ConversationHandler.END


def skip_base_amount(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    logger.info(f'{user_id}: Base amount = None')

    # Get final result
    result = generate_result(records[user_id])
    update.message.reply_text(result)

    return ConversationHandler.END


def cancel(update, context):
    global records
    user_id = update.message.from_user.id
    # user = update.message.from_user

    logger.info(f'{user_id}: Cancelled')
    update.message.reply_text('Bye! Send /start to start over again.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def help(update, context):
    update.message.reply_text('Welcome to Money Changer. Send /start to get started.')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(telegram_bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            BUY_SELL: [MessageHandler(Filters.regex('^(?i)(Buy|Sell)$'), handle_buy_sell)],
            TARGET_CURRENCY: [MessageHandler(Filters.regex('^[a-zA-Z]{3}$'), handle_target_currency)],
            TARGET_AMOUNT: [CommandHandler('skip', skip_target_amount),
                            MessageHandler(Filters.regex('^\d*\.?\d*$'), handle_target_amount)],
            BASE_CURRENCY: [MessageHandler(Filters.regex('^[a-zA-Z]{3}$'), handle_base_currency)],
            BASE_AMOUNT: [CommandHandler('skip', skip_base_amount),
                          MessageHandler(Filters.regex('^\d*\.?\d*$'), handle_base_amount)]
        },

        fallbacks=[CommandHandler('cancel', cancel),
                   CommandHandler('help', help)]
    )

    dp.add_handler(conv_handler)

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    updater.idle()


if __name__ == '__main__':
    main()

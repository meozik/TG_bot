





from telegram.ext import Updater
import logging

updater = Updater(token='694644012:AAEvvizpfI-h9zMQBkru33wKcSOJ8j8Xw2s')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


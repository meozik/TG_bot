import telegram
from telegram.ext import Updater
import logging

my_token = '788115434:AAEUEZ_lcmIYiKeWuDXDJurpL5XeJpfvi8w'
updater = Updater(token=my_token)
dispatcher = updater.dispatcher
bot = telegram.Bot(token=my_token)
print(bot.get_me())
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


meozikChatId = 238813996
def send_message(message):
    # bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
    bot.send_message(chat_id=238813996, text=message)

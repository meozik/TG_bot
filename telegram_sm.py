from telebot import TeleBot
import telegram_send
import logging


my_token = '788115434:AAEjAFnbeSRuB2o5MX4jREeITL7OLH_ka0A'

bot = TeleBot(my_token)
# telegram_send.send(messages=["Wow that was easy!", "pidor"])
print(bot.get_me())
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
bot.send_message(238813996, "dsfdsfds")

# meozikChatId = 238813996
def send_message_to_tg_bot(message):
    telegram_send.send(messages=[message])

import telegram

def send_message_tg():
    bot = telegram.Bot(token='694644012:AAEvvizpfI-h9zMQBkru33wKcSOJ8j8Xw2s')
    print(bot.get_me())
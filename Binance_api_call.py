import requests
import telegram
import json


def parse_price():
    url = 'https://api.binance.com'
    user ='meozik'
    password = 'meozds9205'
    r = requests.get(url+'/api/v1/ticker/24hr')
    return r
def parse_wallet():
    url = 'https://api.binance.com'
    r = requests.get(url + '/api/v3/account',)
def send_message_tg():
    bot = telegram.Bot(token='694644012:AAEvvizpfI-h9zMQBkru33wKcSOJ8j8Xw2s')
    print(bot.get_me())

# print(parse_price().json()[0]['symbol'])
print(parse_price().json())

volume = float(parse_price().json()[0]['volume'])
print(volume)
send_message_tg()
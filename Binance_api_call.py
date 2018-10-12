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

# print(parse_price().json()[0]['symbol'])
# print(parse_price().json())
print(len(parse_price().json()))
pairName = parse_price().json()[0]['symbol']
volume = float(parse_price().json()[0]['volume'])
priceChange = float(parse_price().json()[0]['priceChange'])
print('Pair name =', pairName, 'Volume =', volume, 'Price change', priceChange)

for i in range(len(parse_price().json())-1):
    print(parse_price().json()[i])
    print('Pair name =', pairName, 'Volume =', volume, 'Price change', priceChange)
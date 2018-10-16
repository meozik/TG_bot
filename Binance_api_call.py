import psycopg2 as psycopg2
import requests
import psycopg2
import sys
import sqlite3
import json


def parse_price_json():
    url = 'https://api.binance.com'
    user ='meozik'
    password = 'meozds9205'
    r = requests.get(url+'/api/v1/ticker/24hr')
    return r.json()
def parse_wallet_state():
    url = 'https://api.binance.com'
    r = requests.get(url + '/api/v3/account',)

def db_connect():
    conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')

def db_save(pair_name,price,pricechangepercent,pricechangeabsolut,volume):
    # Коннектимся к локальной базе данных
    conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')
    # Вставляем данные в таблицу
    cursor.execute("""INSERT INTO binance_api_response(pair_name, price, pricechangepercent, pricechangeabsolut, volume)
                          VALUES (?, ?, ?, ?, ?)""", (pair_name, price, pricechangepercent, pricechangeabsolut, volume)
                   )
    # Сохраняем изменения
    conn.commit()


db_save('1',float('0.2'),float('0.213'),float('1.321'),float('1.312321'))


# print(parse_price_json()[0]['symbol'])
print(parse_price_json()[0])


#
# for i in range(len(parse_price_json())):
#     if parse_price_json()[i]['symbol'] == 'TRXBTC':
#         print(i)

# print(len(parse_price_json()))
# pairName = parse_price_json()[0]['symbol']
# volume = float(parse_price_json()[0]['volume'])
# priceChange = float(parse_price_json()[0]['priceChange'])
# print('Pair name =', pairName, 'Volume =', volume, 'Price change', priceChange)

# for i in range(len(parse_price_json())-1):
#     print(parse_price_json()[i])
#     print('Pair name =', pairName, 'Volume =', volume, 'Price change', priceChange)



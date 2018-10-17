import requests
import psycopg2
import time


def get_binance_json():
    url = 'https://api.binance.com'
    user = 'meozik'
    password = 'meozds9205'
    r = requests.get(url + '/api/v1/ticker/24hr')
    return r.json()


def parse_wallet_state():
    url = 'https://api.binance.com'
    r = requests.get(url + '/api/v3/account', )


def db_connect():
    conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')


def db_save(pair_name, price, pricechangepercent, pricechangeabsolut, volume):
    # Коннектимся к локальной базе данных
    conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')
    # Вставляем данные в таблицу
    cursor.execute(f"""INSERT INTO binance_api_response(pair_name, price, pricechangepercent, pricechangeabsolut, volume)
                      VALUES ('{pair_name}', '{price}', '{pricechangepercent}', '{pricechangeabsolut}', '{volume}')"""
                   )
    # Сохраняем изменения
    conn.commit()
    print("Запись произведена успешно!")
    cursor.close()
    del cursor
    conn.close()


def db_update(price, pricechangepercent, pricechangeabsolut, volume):
    # Коннектимся к локальной базе данных
    conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')
    cursor.execute(
        f"""UPDATE binance_api_response SET price = {price}, pricechangepercent = {pricechangepercent}, pricechangeabsolut = {pricechangeabsolut}, volume = {volume} where id=1""")
    # Сохраняем изменения
    conn.commit()
    print("Запись произведена успешно!")
    cursor.close()
    del cursor
    conn.close()

def get_old_volume(i):
    # Коннектимся к локальной базе данных
    conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')
    # Выбираем старые данные по айдишнику валюты
    num = i+1
    cursor.execute(
        f'SELECT volume FROM binance_api_response WHERE id= {num}')
    # Парсим данные в переменную
    result = cursor.fetchall()[i][0]
    cursor.close()
    del cursor
    conn.close()
    return result

def get_price(i):
    avgPrice = (float(get_binance_json()[i]['bidPrice'])+float(get_binance_json()[i]['askPrice']))/2
    return float(avgPrice)

def get_old_price(i):
    # Коннектимся к локальной базе данных
    conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')
    # Выбираем старые данные по айдишнику валюты
    cursor.execute(
        """SELECT price FROM binance_api_response WHERE id={} """.format(int(i)+1))
    # Парсим данные в переменную
    result = cursor.fetchall()[int(i)][0]
    cursor.close()
    del cursor
    conn.close()
    return result

def compare_volume():
    # забираем данные предыдущего значения объема торгов
    old = float(get_old_volume(0))
    print('Старое значение объема', old)
    # Забираем данные нового объема торгов
    new = float(get_binance_json()[0]['quoteVolume'])
    print('Новое значение объема', new)
    # Сравниваем данные
    diff = ((new - old)/old)*100
    if  diff>= 10:
        print('Алярм!!!!')
    print('Разница в процентах',diff)

def compare_price():
    # забираем данные предыдущего значения объема торгов
    old = float(get_old_volume(0))
    print('Старое значение объема', old)
    # Забираем данные нового объема торгов
    new = float(get_binance_json()[0]['quoteVolume'])
    print('Новое значение объема', new)
    # Сравниваем данные
    diff = ((new - old)/old)*100
    if  diff>= 10:
        print('Алярм!!!!')
    print('Разница в процентах',diff)


# compare_volume()
# print(get_binance_json()[0])
print(type(get_old_volume(0)))





# while True:
#     i = 0
#     print(get_binance_json()[i])
#     # db_save(parse_price_json()[0]['symbol'], float('0.0'), float(parse_price_json()[0]['priceChangePercent']),
#     #         float(parse_price_json()[0]['priceChange']), float(parse_price_json()[0]['quoteVolume']))
#     db_update(get_price(i), float(get_binance_json()[i]['priceChangePercent']),
#               float(get_binance_json()[i]['priceChange']), float(get_binance_json()[i]['quoteVolume']))
#     time.sleep(1)

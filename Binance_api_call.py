import requests
import psycopg2
import time
from telegram_sm import send_message_to_tg_bot as send_message

# conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
conn_string = "host='localhost' dbname='binance_bot_db' user='meoz' password='11111111'"


# Тянем данные с /api/v1/ticker/24hr
def get_data():
    url = 'https://api.binance.com'
    r = requests.get(url + '/api/v1/ticker/24hr')
    # print(type(r.status_code))
    print("Стутус код: " + str(r.status_code))
    while r.status_code == 200:
        # print('Function get_data, ', type(r))
        return r
    else:
        time.sleep(30)
        r = requests.get(url + '/api/v1/ticker/24hr')
        return r


# Преобразовываем данные с бэка в json
def get_binance_json():
    x = get_data()
    # print('Type of binanse response object: ', type(x))
    # Приводим тип респонс к джейсону
    data_json = x.json()
    return data_json


# Состояние кошелька(допилить)
def parse_wallet_state():
    url = 'https://api.binance.com'
    r = requests.get(url + '/api/v3/account', )


# Просто коннект к базе
def db_connect():
    # conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    # print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')


# Сохранение в базу строк. !!!!НЕ АПДЕЙТ
def db_save(id, pairname, price, pricechangepercent, pricechangeabsolut, volume):
    # Коннектимся к локальной базе данных
    # conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    # print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('DB_save Connected!\n')
    # Вставляем данные в таблицу
    cursor.execute(f"""INSERT INTO binance_response_data(id, pairname, price, pricechangepercent, pricechangeabsolut, volume)
                      VALUES ('{id}','{pairname}', '{price}', '{pricechangepercent}', '{pricechangeabsolut}', '{volume}')"""
                   )
    # Сохраняем изменения
    conn.commit()
    print("Запись произведена успешно!")
    cursor.close()
    del cursor
    conn.close()


# Апдейт записей в базе, должен происходить каждые пол часа
def db_update(price, pricechangepercent, pricechangeabsolut, volume):
    # Коннектимся к локальной базе данных
    # conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    # print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    # print('db_update connected!\n')
    cursor.execute(
        f"""UPDATE binance_response_data SET price = {price}, pricechangepercent = {pricechangepercent}, pricechangeabsolut = {pricechangeabsolut}, volume = {volume} where id=1""")
    # Сохраняем изменения
    conn.commit()
    # print("Запись произведена успешно!")
    cursor.close()
    del cursor
    conn.close()


# Получение старого значения объема из базы
def get_old_volume(crypto_id):
    # Коннектимся к локальной базе данных
    # conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    # print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('Connected!\n')
    # Выбираем старые данные по айдишнику валюты
    cursor.execute(
        f'SELECT pairname, volume FROM binance_response_data WHERE id= {crypto_id}')
    # Парсим данные в переменную
    result = cursor.fetchall()
    print(result)

    resultVolume, resultPairname = result[0][1], result[0][0]

    # Завершаем сессию
    cursor.close()
    del cursor
    conn.close()
    return resultVolume, resultPairname


# Получение значения цены исходя из медианного в текущем запросе, дальше сохраняется в базу
def get_price(i, json_data):
    avgPrice = (float(json_data[i]['bidPrice']) + float(json_data[i]['askPrice'])) / 2
    return float(avgPrice)


# Получение старого значения price из базы
def get_old_price(i):
    # Коннектимся к локальной базе данных
    # conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    # print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    print('get_old_price Connected!\n')
    # Выбираем старые данные по айдишнику валюты
    cursor.execute(
        """SELECT price FROM binance_response_data WHERE id={} """.format(int(i) + 1))
    # Парсим данные в переменную
    result = cursor.fetchall()[int(i)][0]
    cursor.close()
    del cursor
    conn.close()
    return result


# Сравнение значений предыдущего объема и текущего
def compare_volume(i, quoteVolume, priceDiff, tokenList):
    # забираем данные предыдущего значения объема торгов
    old, pairName = get_old_volume(i)
    print('Старое значение объема для', pairName, old)
    # Забираем данные нового объема торгов
    new = quoteVolume
    print('Новое значение объема для ', pairName, new)
    # Сравниваем данные
    diffVolume = ((new - float(old)) / float(old)) * 100
    if diffVolume >= 50:
        format_message(pairName, diffVolume, priceDiff, tokenList)
    # print('Разница объема в процентах',diff)
    # print('Разница в цене в процентах', priceDiff)


# Сравнение значений предыдущей цены и текущей
def compare_price(i, price):
    # забираем данные предыдущего значения объема торгов
    old = float(get_old_price(i))
    print('Старое значение цены', old)
    # Забираем данные нового объема торгов
    new = get_price(i)
    print('Новое значение цены', new)
    # Сравниваем данные
    diff = ((new - old) / old) * 100
    if diff >= 10:
        print('Алярм!!!!')
    print('Разница цены в процентах', diff)


# Формируем список для дальнейшей отправки одним сообщением в телеграм
def format_message(pair_name, diffVolume, diffPrice, tokenList):
    tokenText = "Торговая пара: " + pair_name + "\n " + "Разница в процентах: " + str(
        diffVolume) + "\n" + "Разница в цене: " + str(diffPrice) + "\n\n"
    tokenList.append(tokenText)


# Отправка нотификаций в телеграмм
# def sendTelegramNotification(tokenList):
#     print('Тут будет выслано сообщение в телегу при срабатывании условия по росту процента объема торгов',pair_name, diff)
#     text = 'Торговая пара: '+ pair_name + '\n '+'Разница в процентах: '+ str(diff)+'\n' + 'Разница в цене: ' + str(priceDiff)
#     send_message(text)

# --------------------------------------Скрипт для записи джейсонины в базу ----------------------------------------
# length= len(token_data)
# for i in range (length):
#     price = get_price(i, token_data)
#     single_token_data = token_data[i]
#     db_save(i, single_token_data['symbol'], price, single_token_data['priceChangePercent'],
#             single_token_data['priceChange'], single_token_data['quoteVolume'])

# --------------------------------------Скрипт для выбора только BTC пар -------------------------------------------
# btc_List = []
#     for i in range(len(token_data)):
#         str1 = str(token_data[i]['symbol'])
#         if str1.startswith('BTC') == True or str1.endswith('BTC') == True:
#             print(str1)
#             btc_List.append(token_data[i])
#     for item in btc_List:
#         print(item)


if __name__ == '__main__':
    token_data = get_binance_json()
    print(token_data)

    # length = 10
    length = len(token_data) - 1
    while True:
        tokenList = []
        for i in range(length):
            single_token_data = token_data[i]
            price = get_price(i, token_data)
            volume = float(single_token_data['quoteVolume'])
            priceDiff = float(single_token_data['priceChangePercent'])
            # compare_volume(i, volume, priceDiff, tokenList)
            # db_update(price, single_token_data['priceChangePercent'],
            #       single_token_data['priceChange'], single_token_data['quoteVolume'])
            # time.sleep(1)
            print('\n\n---------------------------------------------------------------------------')
        text = '\n'.join(tokenList)
        # send_message(text)
        time.sleep(15)

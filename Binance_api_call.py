import requests
import psycopg2
import time


conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"

# Тянем данные с /api/v1/ticker/24hr
def get_data():
    url = 'https://api.binance.com'
    r = requests.get(url + '/api/v1/ticker/24hr')
    print(r.status_code)
    while r.status_code == 200:
        print('Function get_data, ', type(r))
        return r
    else:
        time.sleep(30)
        r = requests.get(url + '/api/v1/ticker/24hr')
        return r

# Преобразовываем данные с бэка вjson
def get_binance_json():
    x = get_data()
    print('Function get_binance json, ',type(x))
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
    cursor.execute(f"""INSERT INTO binance_api_response2(id, pairname, price, pricechangepercent, pricechangeabsolut, volume)
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
    print('db_update connected!\n')
    cursor.execute(
        f"""UPDATE binance_api_response2 SET price = {price}, pricechangepercent = {pricechangepercent}, pricechangeabsolut = {pricechangeabsolut}, volume = {volume} where id=1""")
    # Сохраняем изменения
    conn.commit()
    print("Запись произведена успешно!")
    cursor.close()
    del cursor
    conn.close()

# Получение старого значения объема из базы
def get_old_volume(i):
    # Коннектимся к локальной базе данных
    # conn_string = "host='localhost' dbname='binance_bot_db' user='postgres' password='meozds9205'"
    # print("Connecting to database\n	->%s" % (conn_string))
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    # print('Connected!\n')
    # Выбираем старые данные по айдишнику валюты
    cursor.execute(
        f'SELECT pairname, volume FROM binance_api_response2 WHERE id= {i}')
    # Парсим данные в переменную
    result = cursor.fetchall()
    print(result)
    index = int(i)
    resultVolume, resultPairname = result[index][1], result[index][0]
    # print('resultVolume', resultVolume)
    # print('resultPairname', resultPairname)
    cursor.close()
    del cursor
    conn.close()
    return resultVolume, resultPairname

# Получение значения цены исходя из медианного в текущем запросе, дальше сохраняется в базу
def get_price(i, json_data):
    avgPrice = (float(json_data[i]['bidPrice'])+float(json_data[i]['askPrice']))/2
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
        """SELECT price FROM binance_api_response2 WHERE id={} """.format(int(i)+1))
    # Парсим данные в переменную
    result = cursor.fetchall()[int(i)][0]
    cursor.close()
    del cursor
    conn.close()
    return result


# Сравнение значений предыдущего объема и текущего
def compare_volume(i):
    # забираем данные предыдущего значения объема торгов
    old, pairname = get_old_volume(i)
    print('Старое значение объема', old)
    # Забираем данные нового объема торгов
    new = float(get_binance_json()[i]['quoteVolume'])
    print('Новое значение объема', new)
    # Сравниваем данные
    diff = ((new - float(old))/float(old))*100
    if  diff<= 0:
        sendTelegramNotification(pairname, diff)
    print('Разница объема в процентах',diff)


# Сравнение значений предыдущей цены и текущей
def compare_price(i):
    # забираем данные предыдущего значения объема торгов
    old = float(get_old_price(i))
    print('Старое значение цены', old)
    # Забираем данные нового объема торгов
    new = get_price(i)
    print('Новое значение цены', new)
    # Сравниваем данные
    diff = ((new - old)/old)*100
    if  diff>= 10:
        print('Алярм!!!!')
    print('Разница цены в процентах',diff)


# Отправка нотификаций в телеграмм
def sendTelegramNotification(pair_name, diff):
    print('Тут будет выслано сообщение в телегу при срабатывании условия по росту процента объема торгов',pair_name, diff)

# --------------------------------------Скрипт для записи джейсонины в базу ----------------------------------------
# length= len(token_data)
    # for i in range (length):
    #     price = get_price(i, token_data)
    #     single_token_data = token_data[i]
    #     db_save(i, single_token_data['symbol'], price, single_token_data['priceChangePercent'],
    #             single_token_data['priceChange'], single_token_data['quoteVolume'])

if __name__ == '__main__':
    token_data = get_binance_json()
    length = len(token_data)-1
    while True:
        for i in range (length):
            single_token_data = token_data[i]
            price = get_price(i, token_data)
            compare_volume(i)
            db_update(price, single_token_data['priceChangePercent'],
                  single_token_data['priceChange'], single_token_data['quoteVolume'])
            time.sleep(1)
        time.sleep(15)

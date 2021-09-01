import asyncio
import json
import csv
import time
from os import close, pardir, pipe
from binance import AsyncClient
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

api_key = '8VLvEFhyBTmZOp8XZDLHhuRy0WpFHAlKzp9RLGRN5laRvPB4lmuuC3kDoeK9a14q'
api_secret = 'cZdRIINvixBiMsD4JR81rNYURthJQIjuXvMmIkZaDtno3q1MbHjY9WAuoGZ95KBj'

#output = await client.get_symbol_info("BNBBTC")

#++++++ ВЫНЕСЕННЫЕ ФУНКЦИИ ++++++
async def func_get_products(client):
    products = await client.get_products()
    return products 

async def func_get_my_trades(client, key):
    depth = await client.get_my_trades(symbol=key)
    return depth

async def func_get_open_orders(client, key):
    depth = await client.get_open_orders(symbol=key)
    return depth

async def func_get_exchange_info(client):
    info = await client.get_exchange_info()
    #print(info)
    return info
#++++++ ВЫНЕСЕННЫЕ ФУНКЦИИ ++++++

#универсальная функция, осзволяющая ставить лимитный ордер на покупку или продажу 
async def create_order(client, symbol, side, type, qua, price):
    #покупка
    try:
        buy_limit = await client.create_order(
            symbol = symbol,
            side = side,
            type = type,
            timeInForce = 'GTC',
            quantity = qua,
            price = price)
        with open('perem/order.txt', 'w') as d:
            d.write(json.dumps(buy_limit))
        print(buy_limit)     

    except BinanceAPIException as e:
        # error handling goes here
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#универсальная функция, осзволяющая ставить лимитный ордер на покупку или продажу 

#универсальная функция, осзволяющая ставить OCO ордер на покупку или продажу 
async def create_order_oco(client, symbol, side, qua, price, stopPrice, stopLimitPrice):
    #покупка
    try:
        buy_limit = await client.create_oco_order(
            symbol = symbol,
            side = side,
            quantity = qua,
            price = price,
            stopPrice = stopPrice,
            stopLimitPrice = stopLimitPrice,
            stopLimitTimeInForce = 'GTC'
            )
                #Формируем строку 
        str = ""
        str += f"['{buy_limit['symbol']}', {buy_limit['orderListId']}, '{buy_limit['contingencyType']}', {buy_limit['transactionTime']}, {buy_limit['orders'][0]['orderId']}, {buy_limit['orders'][1]['orderId']}]\n"
        with open('perem/order.txt', 'w') as d:
            #d.write(json.dumps(buy_limit))
            d.write(str)
        #print(json.dumps(buy_limit, indent=2))   

    except BinanceAPIException as e:
        # error handling goes here
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#универсальная функция, осзволяющая ставить OCO ордер на покупку или продажу 


#запрос текущего баланса по не пустым криптовалютам 
async def get_currency(client):
    try:
        avg_price = await client.get_account()
        str = ""
        for key in avg_price["balances"]:
            if key['free'] != '0.00000000' and key['free'] != '0.00':
                str += f"['{key['asset']}', {key['free']}]\n"

        with open('perem/balance.txt', 'w') as d:
            d.write(str)
    except Exception as e:
        print(e)

#выдача актуальных для торговли пар=======================        
async def get_pair(client):
    try:
        #получение всех актуальных пар для нас 
        avg_price = await client.get_account()
        
        arr = []
        pair = []

        for key in avg_price["balances"]:
            if key['free'] != '0.00000000' and key['free'] != '0.00':
                arr.append(key['asset'])
        print(arr)

        with open("perem/limits.txt", 'r') as file:
            inputTXT = file.read()
        #print(inputTXT)
        inputTXT = inputTXT.replace("[", '')
        inputTXT = inputTXT.replace("]", '')
        inputTXT = inputTXT.replace("'", '')
        inputTXT = inputTXT.split("\n")
        i=0
        pair = []
        str = ""
        while i < len(inputTXT) - 1:
            keys = inputTXT[i].split(", ")
            for symbol in arr:
                if symbol == keys[1]:
                    print(keys[0])
                    str += f"['{keys[0]}']\n"
                    pair.append(keys[0])

            i += 1
        #Вывод в файл ответа 
        with open('perem/pair.txt', 'w') as d:
            d.write(f'{str}')
            #d.write(json.dumps(products, indent=2))
        
        #print(string)
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)

#выдача актуальных для торговли пар=======================        


#выдача активных ордеров или всех в принципе=======================   
async def get_orders_func(client, func):
    try:
        #получение всех актуальных пар для нас 
        avg_price = await client.get_account()
        arr = []
        pair = []

        for key in avg_price["balances"]:
            if key['free'] != '0.00000000' and key['free'] != '0.00':
                arr.append(key['asset'])
        #print(arr)
        #time.sleep(3)
        #products = {}
        #products = await func_get_products(client)
                #++++++++++++++++++++++++++++++++
        with open("perem/limits.txt", 'r') as file:
            inputTXT = file.read()
        #print(inputTXT)
        inputTXT = inputTXT.replace("[", '')
        inputTXT = inputTXT.replace("]", '')
        inputTXT = inputTXT.replace("'", '')
        inputTXT = inputTXT.split("\n")
        i=0
        pair = []
        str = ""
        while i < len(inputTXT) - 1:
            keys = inputTXT[i].split(", ")
            for symbol in arr:
                if symbol == keys[1]:
                    #print(keys[0])
                    str += f"[{keys[0]}]\n"
                    pair.append(keys[0])

            i += 1
    #получение всех актуальных пар для нас 
    #получение всех ордеров
        collector = []

        if func == "0":
            for key in pair:
                print(key)
                try:
                    depth = await func_get_my_trades(client, pair)
                    if depth == []:
                        print("Пусто")
                    #print(json.dumps(depth, indent=2))
                    else:
                        #print(json.dumps(depth, indent=2))
                        #print("++++++++")
                        
                        #for key in depth:
                        collector.append(depth)
                        str = ""
                        #print(collector)
                        #if collector != []:
                        for key in collector:
                            print(len(key))
                            for i in key:
                                print(i)
                                #print(i["symbol"], i["orderId"], i["orderListId"], i["price"], i["origQty"], i["type"], i["side"], i["stopPrice"], i["time"], i["isWorking"])
                                #str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['qty']}, '{i['type']}', '{i['side']}', {i['stopPrice']}, {i['time']}, '{i['isWorking']}']\n"
                                str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['qty']}, {i['commission']}, {i['time']}]\n"
                            print(str)

                except:
                    pass
    #получение открытых ордеров
        elif func == "1":
            for key in pair:
                print(key)
                try:
                    depth = await func_get_open_orders(client, pair)
                    if depth == []:
                        print("Пусто")
                    else:
                        #print(json.dumps(depth, indent=2))
                        collector.append(depth)
                        str = ""
                        #print(collector)
                        #if collector != []:
                        for key in collector:
                            for i in key:
                                print(i)
                                #print(i["symbol"], i["orderId"], i["orderListId"], i["price"], i["origQty"], i["type"], i["side"], i["stopPrice"], i["time"], i["isWorking"])
                                str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['origQty']}, '{i['type']}', '{i['side']}', {i['stopPrice']}, {i['time']}, '{i['isWorking']}']\n"
                            
                        print(str)

                except:
                    pass
    #получение открытых ордеров по конкретной паре 
        #Формируем строку 
        #print(json.dumps(depth, indent=2))
        str = ""
        #for key in collector:
            #for i in key:
                #print(i["symbol"], i["orderId"], i["orderListId"], i["price"], i["origQty"], i["type"], i["side"], i["stopPrice"], i["time"], i["isWorking"])
                #str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['origQty']}, '{i['type']}', '{i['side']}', {i['stopPrice']}, {i['time']}, '{i['isWorking']}']\n"
        print(str)
        with open('perem/orders.txt', 'w') as d:
            d.write(str)
        

    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#выдача активных ордеров или всех в принципе=======================   




#выдача активных ордеров или всех в принципе=======================   
async def get_orders_func_pair(client, func, pair):
    try:
        #получение всех актуальных пар для нас 
        collector = []
        if func == "0":
            try:
                depth = await func_get_my_trades(client, pair)
                if depth == []:
                    print("Пусто")
                #print(json.dumps(depth, indent=2))
                else:
                    #print(json.dumps(depth, indent=2))
                    #print("++++++++")
                    
                    #for key in depth:
                    collector.append(depth)
                    str = ""
                    #print(collector)
                    #if collector != []:
                    for key in collector:
                        print(len(key))
                        for i in key:
                            print(i)
                            #print(i["symbol"], i["orderId"], i["orderListId"], i["price"], i["origQty"], i["type"], i["side"], i["stopPrice"], i["time"], i["isWorking"])
                            #str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['qty']}, '{i['type']}', '{i['side']}', {i['stopPrice']}, {i['time']}, '{i['isWorking']}']\n"
                            str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['qty']}, {i['commission']}, {i['time']}]\n"
                        print(str)
            except:
                pass
    #получение открытых ордеров
        elif func == "1":
            try:
                depth = await func_get_open_orders(client, pair)
                if depth == []:
                    print("Пусто")
                else:
                    #print(json.dumps(depth, indent=2))
                    collector.append(depth)
                    str = ""
                    #print(collector)
                    #if collector != []:
                    for key in collector:
                        for i in key:
                            print(i)
                            #print(i["symbol"], i["orderId"], i["orderListId"], i["price"], i["origQty"], i["type"], i["side"], i["stopPrice"], i["time"], i["isWorking"])
                            str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['origQty']}, '{i['type']}', '{i['side']}', {i['stopPrice']}, {i['time']}, '{i['isWorking']}']\n"
                        
                    print(str)
            except:
                pass
    #получение открытых ордеров по конкретной паре 
        '''
        else:
            try:
                depth = await func_get_open_orders(client, func)
                if depth == []:
                    depth = await func_get_my_trades(client, func)
                    if depth == []:
                        print("Пусто")
                    else:
                        collector.append(depth)
                else:
                    collector.append(depth)
                print(json.dumps(depth, indent=2))
            except:
                pass
        '''
        #Формируем строку 
        #print(json.dumps(depth, indent=2))
        '''
        str = ""
        if collector != []:
            for key in collector:
                for i in key:
                    #print(i["symbol"], i["orderId"], i["orderListId"], i["price"], i["origQty"], i["type"], i["side"], i["stopPrice"], i["time"], i["isWorking"])
                    str += f"['{i['symbol']}', {i['orderId']}, {i['orderListId']}, {i['price']}, {i['qty']}, {i['commission']}, {i['time']}]\n"
            print(str)
        '''
        with open('perem/orders.txt', 'w') as d:
            d.write(str)
        

    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#выдача активных ордеров или всех в принципе======================= 





#статус ордера на данный момент=============
async def get_order_status(client, symb, id):
    try:
        order = await client.get_order(symbol=symb, orderId=id)
        #print(json.dumps(order, indent=2))
        #Формируем строку 
        str = ""
        str += f"['{order['symbol']}', {order['orderId']}, {order['orderListId']}, {order['price']}, {order['origQty']}, '{order['type']}', '{order['side']}', {order['stopPrice']}, {order['time']}, '{order['isWorking']}']\n"
        print(str)
        with open('perem/order.txt', 'w') as d:
            d.write(str)
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#статус ордера на данный момент=============

#УДАЛЕНИЕ ордера на данный момент=============
async def del_order_status(client, symb, id):
    try:
        order = await client.cancel_order(symbol=symb, orderId=id)
        #print(json.dumps(order, indent=2))
        #Формируем строку 
        str = ""
        str += f"['{order['symbol']}', {order['orderListId']}, '{order['contingencyType']}', {order['transactionTime']}]\n"
        with open('perem/order_del.txt', 'a') as d:
            d.write(f'{str}')
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#УДАЛЕНИЕ ордера на данный момент=============

#запрос на получение истории по конкретной паре ПО ИНТЕРВАЛУ
async def get_info_param_interval(client, symbol, interval, start, end):
    try:
        klines = await client.get_historical_klines(symbol, interval, start, end)
        print(json.dumps(klines, indent=2))
        with open('perem/spot_margin.txt', 'w') as d:
            for line in klines:
                d.write(f'{line}\n')

    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)

#запрос на получение истории по конкретной паре ОТ СТАРТА ДО НЫНЕШНЕГО ВРЕМЕНИ разница - 6 часов
async def get_info_param_start(client, symbol, interval, start):
    try:
        klines = await client.get_historical_klines(symbol, interval, start)
        print(json.dumps(klines, indent=2))
        with open('perem/spot_margin.txt', 'w') as d:
            for line in klines:
                d.write(f'{line}\n')
                
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)

#Выдача лимитов по запросам и лимитов по парам на ордера 
# Вызывае разово, так как выдаваемый файл слишком большой 
async def get_info_limit(client):
    try:
        data = await func_get_exchange_info(client)
        #print(json.dumps(info, indent=2))
        server_time = data['serverTime']
        print(server_time)
        with open("limit/serverTime.txt", 'w') as d:
            d.write(json.dumps(server_time))
            d.close()

        #for key in data['rateLimits']:
        #    print(key)
        with open("limit/rateLimits.txt", 'w') as d:
            d.write(json.dumps(data['rateLimits'], indent=2))
            d.close()

        #for key in data['symbols']:
        #    print(key)
        with open("limit/symbolsLimits.txt", 'w') as d:
            d.write(json.dumps(data['symbols'], indent=2))
            d.close()

        str = ""      

        for key in data['symbols']:
            str += f"['{key['symbol']}', '{key['baseAsset']}', '{key['quoteAsset']}', {key['filters'][0]['minPrice']}, {key['filters'][0]['maxPrice']}, {key['filters'][2]['minQty']}, {key['filters'][2]['maxQty']}] \n"
        
        print(str)

        with open('perem/limits.txt', 'w') as d:
            d.write(str)

    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#Выдача лимитов по запросам и лимитов по парам на ордера 



# чтение файла input
async def readFileINPUT(client):
    try:
        with open("input.txt", 'r') as file:
            inputTXT = file.read()

        accArr = []
        inputTXT = inputTXT.split("\n")
        i = 0
        #построчно читаем файл как строку
        for n in inputTXT:
            j = 0
            n = n.split(" ")
            #читаем самый первый символ в строке 
            if n[0] == "0":
                #print(len(n), "  =============")
                #print(n)
                # если размер равен 6, то это обычный ордер 
                if len(n) == 6: 
                    n[4] = float(n[4])
                    n[5] = float(n[5])
                    await create_order(client, n[1], n[2], n[3], format(n[3], '.2f'), format(n[5], '.8f'))
                # если размер равен 7, то это OCO ордер 
                elif len(n) == 7:
                    n[3] = float(n[3])
                    n[4] = float(n[4])
                    n[5] = float(n[5])
                    n[6] = float(n[6])
                    await create_order_oco(client, n[1], n[2], format(n[3], '.2f'), format(n[4], '.8f'), format(n[5], '.8f'), format(n[6], '.8f'))
                
            #если  1, то выдача информации по паре за определенный промежуток времени 
            elif n[0] == "1":
                accArr = []
                for key in n:
                    print(key, j)
                    #выбираем строки, которые отвечают за интервал времени 
                    if (j == 3) or (j == 4):
                        #Заменяем разделитель на пробелы 
                        arr_to_str = key.replace("|", " ")
                        #преобразуем в строку 
                        key = ""
                        for str in arr_to_str:
                            key += str
                    #добавляем в массив 
                    accArr.append(key)
                    
                    j += 1
                #Вызов функции на получение истории по конкретной паре
                if len(accArr) == 5:
                    await get_info_param_interval(client, accArr[1], accArr[2], accArr[3], accArr[4])
                elif len(accArr) == 4:
                    await get_info_param_start(client, accArr[1], accArr[2], accArr[3])

            #запрос текущего баланса по не пустым криптовалютам 
            elif n[0] == "2":
                await get_currency(client)

            #выдача актуальных для торговли пар
            elif n[0] == "3":
                await get_pair(client)  

            #выдача активных ордеров или всех в принципе
            elif n[0] == "4":
                #резделяем по пробелам 
                #n = n.split(" ")
                if len(n) == 2:
                    await get_orders_func(client, n[1])
                elif len(n) == 3:
                    await get_orders_func_pair(client, n[1], n[2])
                
            #статус ордера на данный момент
            elif n[0] == "5":
                await get_order_status(client, n[1], n[2])

            #УДАЛЕНИЕ ордера на данный момент
            elif n[0] == "6":
                await del_order_status(client, n[1], n[2])
            
            #Выдача всех лимитов по запросам и ордерам 
            elif n[0] == "7":
                await get_info_limit(client)
            else:
                continue
            i += 1
        #for key in accArr:
        #    print(key)
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
    return accArr



async def main():
    client = await AsyncClient.create(api_key, api_secret)
    #print(client.response.headers)

    #await get_account(client)

    #await create_order(client, 'RVNBTC', 'BUY', 'LIMIT', 200, '0.000001')

    #contents = await readJSONFile("create_order.json")
    #print(type(contents))    

    #for key in contents:
    #    print(key)

#RVNBTC 30m 08|04|2021|10:00:00
    #await get_info_param_start(client, "RVNBTC", "1h", "08.04.2021 3:27:34")

    #for klines in await client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_30MINUTE, "08.04.2021 3:27:34"):
    #    print(klines)



    
#==============================
    getArrInput = await readFileINPUT(client)
#==============================
    



    #orders = await client.get_all_orders(symbol='')
    #print(json.dumps(orders, indent=2))

    #await get_pair(client)

    #await get_orders_func(client, 1)

    #products = await client.get_products()
    #print(products)

    '''
    products = await client.get_exchange_info()
    with open('perem/test.txt', 'w') as d:
        d.write(json.dumps(products, indent=2))
        d.close()
    '''
    #json.loads(perem) преобразует из строки в dict 
    '''
    with open("perem/limits.txt", 'r') as file:
        data = file.read()
    print(type(data))
    data = json.loads(data)
    print(type(data))
    for key in data:
        print(key)
    '''
    '''
    with open("perem/limits.txt", 'r') as file:
        data = file.read()
    data = json.loads(data)
    server_time = data['serverTime']
    print(server_time)
    with open("limit/serverTime.txt", 'w') as d:
        d.write(json.dumps(server_time))
        d.close()

    #for key in data['rateLimits']:
    #    print(key)
    with open("limit/rateLimits.txt", 'w') as d:
        d.write(json.dumps(data['rateLimits'], indent=2))
        d.close()

    #for key in data['symbols']:
    #    print(key)
    with open("limit/symbolsLimits.txt", 'w') as d:
        d.write(json.dumps(data['symbols'], indent=2))
        d.close()
    
    print(data['symbols'][0]['symbol'])
    print(data['symbols'][0]['filters'][0]['minPrice'])
    print(data['symbols'][0]['filters'][0]['maxPrice'])
    
    print(data['symbols'][0]['filters'][2]['minQty'])
    print(data['symbols'][0]['filters'][2]['maxQty'])
    

    str = ""
    str = f"'{data['symbols'][0]['symbol']}', {data['symbols'][0]['filters'][0]['minPrice']}, {data['symbols'][0]['filters'][0]['maxPrice']}, {data['symbols'][0]['filters'][2]['minQty']}, {data['symbols'][0]['filters'][2]['maxQty']}"
    print(str)    

    for key in data['symbols']:
        str += f"['{key['symbol']}', {key['filters'][0]['minPrice']}, {key['filters'][0]['maxPrice']}, {key['filters'][2]['minQty']}, {key['filters'][2]['maxQty']}] \n"
    
    print(str)
    '''

    #with open('data.json', 'w', encoding='utf-8') as f:
    #    json.dump(data, f)

    #await get_order_status(client, "RVNBUSD", "54678013")

    #await del_order_status(client, "RVNBUSD", "54678013")

    #await get_order_status(client, "RVNBUSD", "54678013")

    '''
    while True:
        ret = await func_get_products(client)
        if isinstance(ret, dict):
            print(ret)
            print("dict")
            
        else:
            print("++++++++++++++++")
            break
    '''

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    #input()
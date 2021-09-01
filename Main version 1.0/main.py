import asyncio
import json
import csv
from os import pardir, pipe
from binance import AsyncClient
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

api_key = '8VLvEFhyBTmZOp8XZDLHhuRy0WpFHAlKzp9RLGRN5laRvPB4lmuuC3kDoeK9a14q'
api_secret = 'cZdRIINvixBiMsD4JR81rNYURthJQIjuXvMmIkZaDtno3q1MbHjY9WAuoGZ95KBj'

#запрос текущего баланса по не пустым криптовалютам 
async def get_currency(client):
    try:
        avg_price = await client.get_account()
        arr = []
        for key in avg_price["balances"]:
            if key['free'] != '0.00000000' and key['free'] != '0.00':
                str = f"{key['asset']} {key['free']}"
                arr.append(str)
        for key in arr:
            print(key)

        with open('perem/balance.txt', 'w') as d:
            d.write(json.dumps(arr))
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
        products = await client.get_products()
        #распарсиваем ответ от сервера 
        for key in products["data"]:
            for symbol in arr:
                if symbol == key["b"]:
                    pair.append(key["s"])
                    print(key["s"])


        #формируем нормальный ответ файл 
        index = 0
        string = ""
        for key in pair:
            if index == len(pair) - 1:
                string += f"[{key}]"
            else:
                string += f"[{key}], "
            index += 1
        #Вывод в файл ответа 
        with open('perem/pair.txt', 'w') as d:
            #d.write(f'{string}')
            d.write(json.dumps(products, indent=2))
        
        print(string)
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

        print(arr)
        products = await client.get_products()
        print(products)
        #распарсиваем ответ от сервера 
        for key in products["data"]:
            for symbol in arr:
                if symbol == key["b"]:
                    pair.append(key["s"])
                    print(key["s"])
        #получение всех актуальных пар для нас 
    #получение всех ордеров
        collector = []
        if func == "0":
            for key in pair:
                print(key)
                try:
                    depth = await client.get_my_trades(symbol=key)
                    if depth == []:
                        continue
                    #print(json.dumps(depth, indent=2))
                    collector.append(depth)

                except:
                    pass
    #получение открытых ордеров
        elif func == "1":
            for key in pair:
                print(key)
                try:
                    depth = await client.get_open_orders(symbol=key)
                    if depth == []:
                        continue
                    #print(json.dumps(depth, indent=2))
                    collector.append(depth)

                except:
                    pass
        for key in collector:
            print(key)
        '''
        #формируем нормальный ответ файл 
        index = 0
        string = ""
        for key in pair:
            if index == len(pair) - 1:
                string += f"[{key}]"
            else:
                string += f"[{key}], "
            index += 1
        #Вывод в файл ответа 
        with open('pair.txt', 'w') as d:
            d.write(f'{string}')
        
        print(string)
        '''
        #with open('perem/orders.txt', 'w') as d:
        #    d.write(json.dumps(collector))

        with open('perem/orders.txt', 'w') as d:
            d.write(json.dumps(collector, indent=2))

    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#выдача активных ордеров или всех в принципе=======================   

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

#статус ордера на данный момент=============
async def get_order_status(client, symb, id):
    try:
        order = await client.get_order(symbol=symb, orderId=id)
        print(json.dumps(order, indent=2))

        with open('perem/order.txt', 'a') as d:
            d.write(f'{order}\n')
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)
#статус ордера на данный момент=============

#УДАЛЕНИЕ ордера на данный момент=============
async def del_order_status(client, symb, id):
    try:
        order = await client.cancel_order(symbol=symb, orderId=id)
        print(json.dumps(order, indent=2))

        with open('perem/order.txt', 'a') as d:
            d.write(f'{order}\n')
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


#"1 June, 2021", "30 June, 2021"




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
            #читаем самый первый символ в строке 
            if n[0] == "0":
                #разделяем по пробелам
                n = n.split(" ")
                #добавляем индекс записи 
                accArr.append([i])
                for key in n:
                    #выбиаем строку количества и преобр в тип float
                    if j == 4:
                        key = float(key)
                    accArr[i].append(key)
                    j += 1
            #если  1, то выдача информации по паре за определенный промежуток времени 
            elif n[0] == "1":
                #резделяем по пробелам 
                n = n.split(" ")
                #добавляем индекс записи 
                accArr.append([i])
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
                    accArr[i].append(key)
                    j += 1
                print(len(accArr[i]))

                #Вызов функции на получение истории по конкретной паре
                if len(accArr[i]) == 6:
                    await get_info_param_interval(client, accArr[i][2], accArr[i][3], accArr[i][4], accArr[i][5])
                elif len(accArr[i]) == 5:
                    await get_info_param_start(client, accArr[i][2], accArr[i][3], accArr[i][4])
                
                #print(f"2-й {accArr[i][2]}, 3-й {accArr[i][3]}, 4-й {accArr[i][4]}, 5-й {accArr[i][5]},")
                #Вызов функции на получение истории по конкретной паре
                #await get_info_param(client, accArr[i][2], accArr[i][3], accArr[i][4], accArr[i][5])

            #запрос текущего баланса по не пустым криптовалютам 
            elif n[0] == "2":
                await get_currency(client)

            #выдача актуальных для торговли пар
            elif n[0] == "3":
                await get_pair(client)  

            #выдача активных ордеров или всех в принципе
            elif n[0] == "4":
                #резделяем по пробелам 
                n = n.split(" ")
                await get_orders_func(client, n[1])
                
            #статус ордера на данный момент
            elif n[0] == "5":
                #резделяем по пробелам 
                n = n.split(" ")

                await get_order_status(client, n[1], n[2])

            #УДАЛЕНИЕ ордера на данный момент
            elif n[0] == "6":
                #резделяем по пробелам 
                n = n.split(" ")

                await del_order_status(client, n[1], n[2])

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
    #getArrInput = await readFileINPUT(client)
#==============================

    #orders = await client.get_all_orders(symbol='')
    #print(json.dumps(orders, indent=2))

    #await get_pair(client)

    #await get_orders_func(client, 1)

    #products = await client.get_products()
    #print(products)

    #await get_order_status(client, "RVNBUSD", "54678013")

    #await del_order_status(client, "RVNBUSD", "54678013")

    #await get_order_status(client, "RVNBUSD", "54678013")

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    input()
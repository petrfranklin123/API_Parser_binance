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

#выдача актуальных для торговли пар=======================        
async def get_pair(client):
    try:
        avg_price = await client.get_account()
        arr = []
        slovar = ["USDT", "BUSD", "BNB", "BTC", "TRY"]
        pair = []
    
        for key in avg_price["balances"]:
            if key['free'] != '0.00000000' and key['free'] != '0.00':
                arr.append(key['asset'])

        #сформировываем основные пары 
        for key in arr:
            for slovo in slovar:
                if key != slovo:
                    pair.append(key + slovo)
                else:
                    continue
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
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)

#выдача актуальных для торговли пар=======================        


#выдача активных ордеров или всех в принципе=======================   
async def get_orders_func(client, func):
    try:
        '''
        avg_price = await client.get_account()
        arr = []
        slovar = ["USDT", "BUSD", "BNB", "BTC", "TRY"]
        pair = []
    
        for key in avg_price["balances"]:
            if key['free'] != '0.00000000' and key['free'] != '0.00':
                arr.append(key['asset'])

        #сформировываем основные пары 
        for key in arr:
            for slovo in slovar:
                if key != slovo:
                    pair.append(key + slovo)
                else:
                    continue
        '''
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

        #получение всех актуальных пар для нас 
    #получение всех ордеров
        collector = []
        if func == 0:
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
        elif func == 1:
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
        print("===========")
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
    except Exception as e:
        with open('errors/errors.txt', 'a') as d:
            d.write(f'{e}\n')
        print(e)


#выдача активных ордеров или всех в принципе=======================   


#выдача и запись в файлы данных о кошельке 
async def get_account(client):
    avg_price = await client.get_account()
    arr = []
    arr1 = []
    for key in avg_price["balances"]:
        #print(i)
        #print(key['asset'])
        if key['asset'] == 'BTC':
            #print(key['free'])
            arr.append(key)
        if key['asset'] == 'RVN':
            #print(key['free'])
            arr.append(key)
        
        if key['free'] != '0.00000000' and key['free'] != '0.00':
            arr1.append(key)

    for key in arr:
        print(key)

    with open('btc_bars2.csv', 'w') as d:
        for line in arr:
            d.write(f'{line["asset"]}, {line["free"]}\n')
    
    with open('btc_bars3.csv', 'w') as d:
        for line in arr1:
            d.write(f'{line["asset"]}, {line["free"]}\n')

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
        await writeFileOutput(buy_limit)
        print(buy_limit)     

    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)

#запрос текущего курса по не пустым криптовалютам 
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
        await writeFileOutput(arr)
    except Exception as e:
        print(e)
    


#получение обфчного файла 
async def readFile(name):
    with open(name, "r") as file:
        contents = file.read()
    return contents

#получение json файла 
async def readJSONFile(name):
    with open(name, 'r') as file:
        jsonn = json.load(file)
    return jsonn
'''
# чтение файла input
async def readFileINPUT():
    with open("input.txt", 'r') as file:
        inputTXT = file.read()

    accArr = []
    inputTXT = inputTXT.split("\n")
    i = 0
    for n in inputTXT:
        accArr.append([i])
        n = n.split(" ")
        j = 0
        for key in n:
            if j == 4:
                key = float(key)
            accArr[i].append(key)
            j += 1
        i += 1
    for key in accArr:
        print(key)
    return accArr
'''

# чтение файла input
async def readFileINPUT(client):
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
            
            #Вызов функции на получение истории по конкретной паре
            await get_info_param(client, accArr[i][2], accArr[i][3], accArr[i][4], accArr[i][5])
            
        i += 1

        '''
        n = n.split(" ")
        #print(n)
        accArr.append([i])

        j = 0
        #если 0, то устанавливаем ордер 
        if n[0] == "0":
            print("-----0------")
            for key in n:
                
                if j == 4:
                    key = float(key)
                accArr[i].append(key)
                j += 1
        #если  1, то выдача информации по паре за определенный промежуток времени 
        elif n[0] == "1":
            #print(n)
            print("-----1------")
            print(n[0], n[1], n[2], n[3])

        i += 1
        '''
    for key in accArr:
        print(key)
    return accArr

    '''
    #блок добления на условия для дальнейшего последовательноо сценария 
    for key in getArrInput:
        #если 0, то устанавливаем ордер 
        if key[1] == '0':
            #await create_order(client, key[2], key[3], key[4], key[5], key[6])
            await create_order(client, "RVNBNB", "SELL", "LIMIT", 195.0, "0.00034")
        #если  1, то выдача информации по паре за определенный промежуток времени 
        elif key[1] == '1':
            await get_info_param(client, "RVNBTC", "1h", "1 June, 2021", "23 July, 2021")
    '''
#очистка файла 
async def clearFile():
    with open('input.txt', 'w') as d:
        d.write("")

#запись ответа в output
async def writeFileOutput(mess):
    with open('perem/output.txt', 'w') as d:
        d.write(json.dumps(mess))

#запрос на получение истории по конкретной паре 
async def get_info_param(client, symbol, interval, start, end):
    klines = await client.get_historical_klines(symbol, interval, start, end)
    print(json.dumps(klines, indent=2))
    with open('spot_margin.txt', 'w') as d:
        for line in klines:
            d.write(f'{line}\n')

#"1 June, 2021", "30 June, 2021"


'''
Это все часть асинхронного запроса 

get_account(**params) достать из этой функции весь баланс 
'''
async def main():
    client = await AsyncClient.create(api_key, api_secret)
    #print(client.response.headers)

    #await get_account(client)

    #await create_order(client, 'RVNBTC', 'BUY', 'LIMIT', 200, '0.000001')

    #contents = await readJSONFile("create_order.json")
    #print(type(contents))    

    #for key in contents:
    #    print(key)

    #await get_info_param(client, "RVNBTC", "1h", "1 June, 2021", "23 July, 2021")



    
#==============================
    #getArrInput = await readFileINPUT(client)
#==============================

    #orders = await client.get_all_orders(symbol='')
    #print(json.dumps(orders, indent=2))

    #await get_pair(client)

    await get_orders_func(client, 0)










    '''
    #получение всех актуальных пар для нас 
    avg_price = await client.get_account()
    arr = []
    pair = []

    for key in avg_price["balances"]:
        if key['free'] != '0.00000000' and key['free'] != '0.00':
            arr.append(key['asset'])

    products = await client.get_products()
    #распарсиваем ответ от сервера 
    for key in products["data"]:
        for symbol in arr:
            if symbol == key["b"]:
                pair.append(key["s"])
                print(key["s"])

    #получение всех актуальных пар для нас 
    '''














    #print(json.dumps(products, indent=2))
    
    #for mass in products:
    #    for key in mass:
    #        print(key)
    '''
    symb = "RVNBTC"
    depth = await client.get_my_trades(symbol=symb)
    print(json.dumps(depth, indent=2))
    '''
    '''
    #Выдача ордеров на данный момент
    try:
        depth = await client.get_order_book(symbol='BNBBTC')
        print(json.dumps(depth, indent=2))
    except Exception as e:
        print(e)
    '''

    '''
    #блок добления на условия для дальнейшего последовательноо сценария 
    for key in getArrInput:
        #если 0, то устанавливаем ордер 
        if key[1] == '0':
            #await create_order(client, key[2], key[3], key[4], key[5], key[6])
            await create_order(client, "RVNBNB", "SELL", "LIMIT", 195.0, "0.00034")
        #если  1, то выдача информации по паре за определенный промежуток времени 
        elif key[1] == '1':
            await get_info_param(client, "RVNBTC", "1h", "1 June, 2021", "23 July, 2021")
    '''

#==============================
    

    #await get_currency(client)



    '''
    #get_all_tickers() → List[Dict[str, str]]
    #список -> словарь 
    avg_price = await client.get_account()
    arr = []
    arr1 = []
    for key in avg_price["balances"]:
        #print(i)
        #print(key['asset'])
        if key['asset'] == 'BTC':
            #print(key['free'])
            arr.append(key)
        if key['asset'] == 'RVN':
            #print(key['free'])
            arr.append(key)
        
        if key['free'] != '0.00000000' and key['free'] != '0.00':
            arr1.append(key)

    for key in arr:
        print(key)

    with open('btc_bars2.csv', 'w') as d:
        for line in arr:
            d.write(f'{line["asset"]}, {line["free"]}\n')
    
    with open('btc_bars3.csv', 'w') as d:
        for line in arr1:
            d.write(f'{line["asset"]}, {line["free"]}\n')
    '''

    '''
    for keys,values in avg_price.items():
        if values == "MLN":
            print(keys)
            print(values)
        if keys == "MLN":
            print(keys)
            print(values)
    '''
    '''
    #покупка
    try:
        buy_limit = await client.create_order(
            symbol='RVNBTC',
            side='BUY',
            type='LIMIT',
            timeInForce='GTC',
            quantity=200,
            price='0.000001')

    except BinanceAPIException as e:
        # error handling goes here
        print(e)
    except BinanceOrderException as e:
        # error handling goes here
        print(e)

    print(buy_limit)
    '''
    '''
    #выдать все открытые ордера 
    orders = await client.get_open_orders(symbol='RVNBTC')
    print(json.dumps(orders, indent=2))

    #выдать ордер по конкретному id 
    order = await client.get_order(symbol='RVNBTC', orderId=131134106)
    print(json.dumps(order, indent=2))

    #отменить заказ 
    result = await client.cancel_order(symbol='RVNBTC', orderId=131134106)
    print(json.dumps(result, indent=2))

    #tickers = await client.get_ticker()
    #print(json.dumps(tickers, indent=2))
    '''

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    input()
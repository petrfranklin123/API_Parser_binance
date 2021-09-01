import asyncio
import json
import csv
from binance import AsyncClient
from binance.client import Client
from binance.enums import *

api_key = '8VLvEFhyBTmZOp8XZDLHhuRy0WpFHAlKzp9RLGRN5laRvPB4lmuuC3kDoeK9a14q'
api_secret = 'cZdRIINvixBiMsD4JR81rNYURthJQIjuXvMmIkZaDtno3q1MbHjY9WAuoGZ95KBj'

'''
Это все часть асинхронного запроса 
'''
async def main():
    client = await AsyncClient.create(api_key, api_secret)
    #print(client.response.headers)

    #res = await client.get_exchange_info()
    #print(json.dumps(res, indent=2))
    
#получение информации о паре и их лимитах на покупку и продажу
    info = await client.get_symbol_info('BNBBTC')
    print(json.dumps(info, indent=2))

#комиссия по валюте    
    #info = await client.get_trade_fee()
    #print(json.dumps(info, indent=2))
    info = json.dumps(info, indent=2)
    with open('btc_bars2.csv', 'w') as d:
            d.write(f'{info}\n')


    #info = await client.get_my_trades('RVNBTC')
    #print(json.dumps(info, indent=2))


#Значение всех валют на данный момент 
    #info = await client.get_all_tickers()
    #print(json.dumps(info, indent=2))


    #info = await client.get_account_snapshot(type='SPOT')
    #print(json.dumps(info, indent=2))

#Вернуть список продуктов, которые в настоящее время перечислены на Binance
    #products = await client.get_products()
    #print(json.dumps(products, indent=2))

#Выдача ордеров на данный момент
    #depth = await client.get_order_book(symbol='BNBBTC')
    #print(json.dumps(depth, indent=2))

# Получить последние сделки
    #trades = await client.get_recent_trades(symbol='BNBBTC')
    #print(json.dumps(trades, indent=2))

# Получить последние сделки (вроде бы то же самое)
    #trades = await client.get_historical_trades(symbol='BNBBTC')
    #print(json.dumps(trades, indent=2))

    #trades = await client.get_aggregate_trades(symbol='BNBBTC')
    #print(json.dumps(trades, indent=2))

#получение курса 
    #candles = await client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
    #print(json.dumps(candles, indent=2))

#история получение дипозита 
    #avg_price = await client.get_deposit_history()
    #print(json.dumps(avg_price, indent=2))

#получение ордеров (если отправлять пустую облать, то выведет все ордера)
    #orders = await client.get_open_orders(symbol='RVNBTC')
    #print(json.dumps(orders, indent=2))

#Статистика изменения цен за 24 часа
    #tickers = await client.get_ticker()
    #print(json.dumps(tickers, indent=2))

    # получить 1 минуту klines за последний день до настоящего момента
    #klines = await client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    # получить 30 минут klines за последний месяц 2017 года
    #klines = await client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2020", "30 June, 2021")

    # получать еженедельные klines, поскольку он перечислил
    #klines = await client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")

    #print(json.dumps(klines, indent=2))
    #with open('btc_bars.txt', 'w') as d:
    #    for line in klines:
    #        d.write(f'{line}\n')
    '''
    avg_price = await client.get_avg_price(symbol='BNBBTC')
    print(json.dumps(avg_price, indent=2))
    print(avg_price)
    print(type(avg_price))
    print(avg_price["mins"])
    '''

    '''
    avg_price = json.dumps(avg_price, indent=2)
    print(type(avg_price))
    print(len(avg_price))
    '''

    '''
    #get_all_tickers() → List[Dict[str, str]]
    #список -> словарь 
    avg_price = await client.get_account()
    #print(json.dumps(avg_price, indent=2))
    #print(type(avg_price))
    #for key in avg_price:
    #    print(key)
    arr = []
    for key in avg_price["balances"]:
        #print(i)
        #print(key['asset'])
        if key['asset'] == 'BTC':
            #print(key['free'])
            arr.append(key)
        if key['asset'] == 'RVN':
            #print(key['free'])
            arr.append(key)
    for key in arr:
        print(key)

    with open('btc_bars2.csv', 'w') as d:
        for line in arr:
            d.write(f'{line["asset"]}, {line["free"]}\n')
    '''

    #orders = await client.get_open_orders(symbol='RVNBTC')
    #print(json.dumps(orders, indent=2))

    #купить 
    #order = await client.order_limit_buy(
    #    symbol='RVNBTC',
    #    quantity=70,
    #    price='0,0000017')
    #print(json.dumps(order, indent=2))

    '''
    for keys,values in avg_price.items():
        if values == "MLN":
            print(keys)
            print(values)
        if keys == "MLN":
            print(keys)
            print(values)
    '''

    #tickers = await client.get_ticker()
    #print(json.dumps(tickers, indent=2))

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
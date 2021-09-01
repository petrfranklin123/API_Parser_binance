import asyncio
import json
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
    

    #info = await client.get_symbol_info('BNBBTC')
    #print(json.dumps(info, indent=2))

    #info = await client.get_all_tickers()
    #print(json.dumps(info, indent=2))

    #info = await client.get_account_snapshot(type='SPOT')
    #print(json.dumps(info, indent=2))

    #products = await client.get_products()
    #print(json.dumps(products, indent=2))

    #depth = await client.get_order_book(symbol='BNBBTC')
    #print(json.dumps(depth, indent=2))

    #trades = await client.get_recent_trades(symbol='BNBBTC')
    #print(json.dumps(trades, indent=2))

    #trades = await client.get_historical_trades(symbol='BNBBTC')
    #print(json.dumps(trades, indent=2))

    #trades = await client.get_aggregate_trades(symbol='BNBBTC')
    #print(json.dumps(trades, indent=2))

    #candles = await client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
    #print(json.dumps(candles, indent=2))

    # fetch 1 minute klines for the last day up until now
    #klines = await client.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    # fetch 30 minute klines for the last month of 2017
    #klines = await client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

    # fetch weekly klines since it listed
    #klines = await client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
    #print(json.dumps(klines, indent=2))
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
    #avg_price = await client.get_deposit_history()
    #print(json.dumps(avg_price, indent=2))

    #get_all_tickers() → List[Dict[str, str]]
    #список -> словарь 
    avg_price = await client.get_account()
    #print(json.dumps(avg_price, indent=2))
    #print(type(avg_price))
    #for key in avg_price:
    #    print(key)
    i = 0
    for key in avg_price["balances"]:
        #print(i)
        #print(key['asset'])
        if key['asset'] == 'BTC':
            print(key['free'])
        if key['asset'] == 'RVN':
            print(key['free'])
        i += 1


    orders = await client.get_open_orders(symbol='RVNBTC')
    print(json.dumps(orders, indent=2))

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
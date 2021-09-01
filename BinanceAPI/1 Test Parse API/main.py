import asyncio
import json
from binance import AsyncClient
from binance.client import Client
#from binance.websockets import BinanceSocketManager

async def main():
    client = await AsyncClient.create()

    # fetch exchange info
    #res = await client.get_exchange_info()
    #print(json.dumps(res, indent=2))

    klines = await client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2020", "10 July, 2021")
    print(json.dumps(klines, indent=2))

    #info = await client.get_symbol_info('BNBBTC')
    #print(json.dumps(info, indent=2))

    #for kline in client.get_historical_klines_generator("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC"):
    #    print(kline)

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
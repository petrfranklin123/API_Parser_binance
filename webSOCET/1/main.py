# pip install websockets

import websockets
import asyncio
import json
import time
import matplotlib.pyplot as plt

#веб сокеты, отлричаются от HTTP тем, что они постоянно включены 

async def main():
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    #url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    #открываем контекстный менеджер 
    async with websockets.connect(url) as client:
        while True:
            #получаем джейсон файл, распарисм его в обычный объект
            data = json.loads(await client.recv())['data']
            # берем время на бирже и преобразуем в обычное время 
            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"
            # записываем значние времени и значение курса 
            print(event_time, data['c'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
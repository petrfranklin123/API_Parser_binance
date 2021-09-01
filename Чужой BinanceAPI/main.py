from binance_api import Binance
bot = Binance(
    API_KEY='8VLvEFhyBTmZOp8XZDLHhuRy0WpFHAlKzp9RLGRN5laRvPB4lmuuC3kDoeK9a14q',
    API_SECRET='cZdRIINvixBiMsD4JR81rNYURthJQIjuXvMmIkZaDtno3q1MbHjY9WAuoGZ95KBj'
)
#print(bot.ping())
#print(bot.time())
'''
print('klines', bot.klines(
    symbol='BNBBTC',
    interval='5m',
    limit=500
))
'''
'''
print('ticker/price', bot.tickerPrice(
    symbol='BNBBTC'
))
'''
#for key in bot.klines(symbol='BNBBTC', interval='5m', limit=500):
#    print(key)
'''
print('myTrades', bot.myTrades(
    symbol='RVNBTC'
))
'''
'''
print('allOrders', bot.allOrders(
    symbol='RVNBTC',
))
'''
# Все открытые ордера по паре
print('openOrders', bot.openOrders(
    symbol='RVNBTC',
))

# Все открытые ордера по всем парам
print('openOrders', bot.openOrders())
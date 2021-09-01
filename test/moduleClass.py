class CoinsBinance(object):
#    def __init__(self, url):
#        self.url_coins = []
#        self.url_coins.append(url)

    def __init__(self):
        self.url_coins = []

    def set_url(self, url):
        self.url_coins.append(url)

    def get_all_url(self):
        out = ""
        for url in self.url_coins:
            out = out + ", " + url
        print(out)
    
    def __str__(self):
        return f"{self.url_coins}"

class Coin(object):
    def __init__(self, glass_price, glass_col, glass_all):
        
        pass
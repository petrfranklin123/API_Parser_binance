#программа отключения webdriver 

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
#import random 
from selenium.webdriver.common.keys import Keys
#ожидание подгркзки элементов 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#import moduleClass
#import function


driver = webdriver.Chrome()

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


def waitCSS(driver, search):
    return WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_css_selector(search))

def waitCSSs(driver, search):
    return WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_css_selector(search))

def waitXPATH(driver, search):
    #print(search)
    #print(WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(search)).text)
    return WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(search))

def waitXPATHs(driver, search):
    return WebDriverWait(driver, 10).until(lambda driver: driver.find_elements_by_xpath(search))

def parse_glass_sale_XPATH(col):
    i = 0
    glass_arr = []
    #print("++++")
    while i < 16:
        glass_arr.append(waitXPATH(driver, f'//*[@id="spotOrderbook"]/div[3]/div[1]/div[1]/div[1]/div/div[{i+1}]/div/div[1]/div[{col}]').text)
        i += 1
    return glass_arr

def parse_glass_buy_XPATH(col):
    i = 0
    glass_arr = []
    #print("++++")//*[@id="spotOrderbook"]/div[3]/div[3]/div[1]/div[1]/div/div[1]/div/div[1]/div[1]
    while i < 16:
        glass_arr.append(waitXPATH(driver, f'//*[@id="spotOrderbook"]/div[3]/div[3]/div[1]/div[1]/div/div[{i+1}]/div/div[1]/div[{col}]').text)
        i += 1
    return glass_arr

def table_glass(glass_price, glass_col, glass_all):
    i = 0 
    print("Цена        Количество   Всего")
    while i < len(glass_price):
        print(glass_price[i], "   ", glass_col[i], "   ", glass_all[i], "   ",)
        i += 1

def show_coin(driver):
    return waitXPATH(driver, '//*[@id="__APP"]/div/div/div[4]/div/div[1]/div[1]/div/div[1]/div/div[1]/div/h1')

def show_coin_price(driver):
    return waitXPATH(driver, '//*[@id="__APP"]/div/div/div[4]/div/div[1]/div[1]/div/div[2]/div[1]')

def show_coin_and_price(driver):
    coin = show_coin(driver)
    price = show_coin_price(driver)

    print(" Название криптовалюты : ", coin.text, " ; Цена за одну штуку : ", price.text )

def parse_coin(url):
    show_coin_and_price(driver)

    glass_price_sale = []
    glass_col_sale = []
    glass_all_sale = []

    glass_price_sale = parse_glass_sale_XPATH(1)
    glass_col_sale = parse_glass_sale_XPATH(2)
    glass_all_sale = parse_glass_sale_XPATH(3)
                                      
    table_glass(glass_price_sale, glass_col_sale, glass_all_sale)

    glass_price_buy = []
    glass_col_buy = []
    glass_all_buy = []

    glass_price_buy = parse_glass_buy_XPATH(1)
    glass_col_buy = parse_glass_buy_XPATH(2)
    glass_all_buy = parse_glass_buy_XPATH(3)
                                      
    table_glass(glass_price_buy, glass_col_buy, glass_all_buy)

#--------------------Табуляция окна
def tab_window(window):
    driver.switch_to.window(driver.window_handles[window])

#//*[@id="spotOrderbook"]/div[3]/div[1]/div[1]/div[1]/div/div[16]/div/div[1]/div[1]
#если все отработало корректно 

def main():
    #option = webdriver.ChromeOptions()

    url1 = ["https://www.binance.com/ru/trade/BNB_RUB?type=spot", "https://www.binance.com/ru/trade/DOGE_BUSD?type=spot", "https://www.binance.com/ru/trade/ETH_BUSD?type=spot"]
    #для старых браузеров
    #option.add_experimental_option("excludeSwitches", ["enable-automation"])
    #option.add_experimental_option("useAutomationExtension", False)

    #для новых браузеров 
    #option.add_argument("--disable-blink-features=AutomationControlled")

    #фоновый режим 
    #option.add_argument("--headless")
    #option.headless = True

    #driver = webdriver.Chrome(options=option)



    try:
        #ссылка на просмотр данных об режиме браузера 
        driver.get(url1[0])
        #driver.get(url1[1])

        position = 1
        for url in url1:
            driver.execute_script(f"window.open('{url}')")
            driver.switch_to.window(driver.window_handles[position])
            parse_coin(driver)
            
            #print(driver.window_handles)
            position += 1
        
        position = 1
        while 1:
            if position > len(url1):
                position = 1
            else:
                driver.switch_to.window(driver.window_handles[position])
                parse_coin(url1[0])
                position += 1



#----------------Выдача парсинга
        #parse_coin(url1)



#----------------Выдача всех ссылок
        coins = CoinsBinance()
        for url in url1:
            coins.set_url(url)

        coins.get_all_url()

        #print(coins)
        
        #for elem in glass_price:
        #   print(elem)

        time.sleep(10)

        '''
        #search = driver.find_element_by_id("search")

        #количество открытых вкладок 
        print(driver.window_handles)
        #url текущей вкладки
        print(f"URL is : {driver.current_url}")

        search.send_keys("Видеокарты")
        search.send_keys(Keys.ENTER)
        #time.sleep(3)

        #количество открытых вкладок 
        print(driver.window_handles)
        #url текущей вкладки
        print(f"URL is : {driver.current_url}")

        #получаем список из объявлений
        #items = driver.find_elements_by_xpath("//div[@data-marker='item-photo']")
        items = waitXPATHs(driver, "//div[@data-marker='item-photo']")
        items[0].click()

        #time.sleep(3)
        #обязательно делаем переход, иначе мы будем, формально, на прошлой странице
        driver.switch_to.window(driver.window_handles[1])

        #количество открытых вкладок 
        print(driver.window_handles)
        #url текущей вкладки
        print(f"URL is : {driver.current_url}")

        #получаем имя владельца поста 
        user_name = waitCSS(driver, ".seller-info-name")
        print(f"User is name : {user_name.text}")
        #time.sleep(3)

        #закрываем открытое окно 
        driver.close()

        #чтобы не возникло ошибок, переходим на первую вкладку 
        driver.switch_to.window(driver.window_handles[0])
        #time.sleep(3)
        print(f"URL is : {driver.current_url}")


        #заходим на новую вкладку 
        items[1].click()
        #обязательно делаем переход, иначе мы будем, формально, на прошлой странице
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        user_name = driver.find_element_by_xpath("//div[@data-marker='seller-info/name']")
        print(f"User is name : {user_name.text}")

        ad_date = driver.find_element_by_class_name("title-info-metadata-item-redesign")
        print(f"An ad date is : {ad_date.text}")

        joined_date = driver.find_element_by_class_name("seller-info-value")
        print(f"User since : {joined_date.text}")
        '''
        '''
        #переход на первую вкладку
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        items[1].click()
        #количество открытых вкладок 
        print(driver.window_handles)
        #url текущей вкладки
        print(f"URL is : {driver.current_url}")
        time.sleep(5)
        '''


    #обработка исключения 
    except Exception as ex:
        print(ex)

    #выполняем всегда 
    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
    main()
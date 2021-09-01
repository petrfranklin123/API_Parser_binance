from selenium import webdriver
import time
from selenium.webdriver.common.by import By
#import random 
from selenium.webdriver.common.keys import Keys
#ожидание подгркзки элементов 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#driver = webdriver.Chrome()
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

def parse_glass_sale_XPATH(driver, col):
    i = 0
    glass_arr = []
    #print("++++")
    while i < 16:
        glass_arr.append(waitXPATH(driver, f'//*[@id="spotOrderbook"]/div[3]/div[1]/div[1]/div[1]/div/div[{i+1}]/div/div[1]/div[{col}]').text)
        i += 1
    return glass_arr

def parse_glass_buy_XPATH(driver, col):
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

def parse_coin(driver):
    show_coin_and_price(driver)

    glass_price_sale = []
    glass_col_sale = []
    glass_all_sale = []

    glass_price_sale = parse_glass_sale_XPATH(driver, 1)
    glass_col_sale = parse_glass_sale_XPATH(driver, 2)
    glass_all_sale = parse_glass_sale_XPATH(driver, 3)
                                      
    table_glass(glass_price_sale, glass_col_sale, glass_all_sale)

    glass_price_buy = []
    glass_col_buy = []
    glass_all_buy = []

    glass_price_buy = parse_glass_buy_XPATH(driver, 1)
    glass_col_buy = parse_glass_buy_XPATH(driver, 2)
    glass_all_buy = parse_glass_buy_XPATH(driver, 3)
                                      
    table_glass(glass_price_buy, glass_col_buy, glass_all_buy)

#--------------------Табуляция окна
def tab_window(driver, window):
    driver.switch_to.window(driver.window_handles[window])

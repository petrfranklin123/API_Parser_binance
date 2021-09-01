from selenium import webdriver

def main():
    driver = webdriver.Chrome()
    driver.get("https://proghub.ru/")
    btn_elem = driver.find_element_by_class_name("call-action")
    btn_elem.click()

if __name__ == "__main__":
    main()
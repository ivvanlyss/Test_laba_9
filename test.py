from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
import time
import pytest

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
    
    def find(self, locator):
        return self.driver.find_element(*locator)
    
    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
    
    def click(self, locator):
        self.find(locator).click()

class OrderPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://127.0.0.1:8000"
    
    def open(self):
        self.driver.get(self.url)
        time.sleep(1)
        return self
    
    name_field = (By.NAME, "name")
    email_field = (By.NAME, "email") 
    phone_field = (By.NAME, "phone")
    address_field = (By.NAME, "address")
    pay_select = (By.NAME, "pay_method")
    agree_check = (By.NAME, "agree")
    submit_btn = (By.XPATH, "//button[@type='submit']")
    error_msg = (By.CLASS_NAME, "error")
    success_msg = (By.CLASS_NAME, "success")
    
    def fill_name(self, name):
        self.type(self.name_field, name)
        return self
    
    def fill_email(self, email):
        self.type(self.email_field, email)
        return self
    
    def fill_phone(self, phone):
        self.type(self.phone_field, phone)
        return self
    
    def fill_address(self, address):
        self.type(self.address_field, address)
        return self
    
    def select_payment(self, method):
        select = Select(self.find(self.pay_select))
        select.select_by_value(method)
        return self
    
    def check_agree(self):
        if not self.find(self.agree_check).is_selected():
            self.click(self.agree_check)
        return self
    
    def uncheck_agree(self):
        if self.find(self.agree_check).is_selected():
            self.click(self.agree_check)
        return self
    
    def submit(self):
        self.click(self.submit_btn)
        time.sleep(1)
        return self
    
    def get_errors(self):
        try:
            return self.find(self.error_msg).text
        except:
            return None
    
    def get_success(self):
        try:
            return self.find(self.success_msg).text
        except:
            return None

def test_good_order():
    """Тест 1: правильное заполнение формы"""
    # Настройка Chrome для headless-режима (без графического интерфейса)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    page = OrderPage(driver)
    
    try:
        page.open()
        page.fill_name("Петров Петр")
        page.fill_email("petr@mail.ru")
        page.fill_phone("89991234567")
        page.fill_address("Москва, ул. Ленина 1")
        page.select_payment("card")
        page.check_agree()
        page.submit()
        
        time.sleep(2)
        
        # Используем assert для проверки результатов теста
        success_indicator = "success" in driver.page_source.lower() or "заказ принят" in driver.page_source.lower()
        assert success_indicator, "Тест не пройден: сообщение об успехе не найдено"
        print("Тест 1 пройден: правильное заполнение формы работает корректно")
            
    finally:
        driver.quit()

def test_bad_order():
    """Тест 2: неправильное заполнение (пустое имя)"""
    # Настройка Chrome для headless-режима
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    page = OrderPage(driver)
    
    try:
        page.open()
        # Намеренно не заполняем поле имени
        page.fill_email("test@test.ru")
        page.fill_phone("89991112233")
        page.select_payment("cash")
        page.check_agree()
        page.submit()
        
        time.sleep(2)
        
        # Проверяем наличие ошибки
        errors = page.get_errors()
        error_found = errors and ("фио" in errors.lower() or "имя" in errors.lower())
        assert error_found, "Тест не пройден: ошибка для пустого имени не найдена"
        print("Тест 2 пройден: валидация пустого имени работает корректно")
            
    finally:
        driver.quit()

if __name__ == "__main__":
    # Запуск тестов при прямом выполнении файла
    test_good_order()
    test_bad_order()
    print("\nВсе тесты выполнены успешно!")
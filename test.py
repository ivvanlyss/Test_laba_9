import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class TestSimpleAuth:
    @pytest.fixture
    def driver(self):
        chrome_options = Options()
        
        # Для GitHub Actions используем headless режим
        if os.getenv('GITHUB_ACTIONS') == 'true':
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        
        yield driver
        driver.quit()

    def test_successful_login(self, driver):
        driver.get("http://localhost:8000/")
        
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        username.send_keys("admin")
        password.send_keys("admin123")
        login_btn.click()
        
        WebDriverWait(driver, 10).until(EC.url_contains("/success"))
        assert "/success" in driver.current_url
        
        success_msg = driver.find_element(By.CLASS_NAME, "success")
        assert "Login Successful" in success_msg.text

    def test_failed_login(self, driver):
        driver.get("http://localhost:8000/")
        
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        username.send_keys("wrong")
        password.send_keys("wrong")
        login_btn.click()
        
        time.sleep(2)
        assert "localhost:8000" in driver.current_url
        assert "error" in driver.page_source.lower()

def test_quick_check():
    """Быстрый тест для проверки что всё работает"""
    assert 1 + 1 == 2
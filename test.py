import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

class TestSimpleAuth:
    @pytest.fixture
    def driver(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.implicitly_wait(5)
        yield driver
        driver.quit()

    def test_successful_login(self, driver):
        print("\nTesting successful login...")
        
        driver.get("http://127.0.0.1:8000/")
        
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        assert username_field.is_displayed()
        assert password_field.is_displayed()
        assert login_button.is_displayed()
        print("Login form elements are present")

        username_field.send_keys("admin")
        password_field.send_keys("admin123")
        login_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("/success")
        )
        
        success_message = driver.find_element(By.CLASS_NAME, "success")
        assert "Login Successful" in success_message.text
        print("Success page loaded correctly")

        logout_link = driver.find_element(By.CLASS_NAME, "logout")
        assert logout_link.is_displayed()
        print("Logout link is present")

    def test_failed_login(self, driver):
        print("\nTesting failed login...")
        
        driver.get("http://127.0.0.1:8000/")
        
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        
        username_field.send_keys("wronguser")
        password_field.send_keys("wrongpass")
        login_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "error"))
        )
        
        error_message = driver.find_element(By.CLASS_NAME, "error")
        assert "Invalid username or password" in error_message.text
        print("Error message displayed correctly")

        assert "127.0.0.1:8000/" in driver.current_url
        print("Stayed on login page after failed attempt")

    def test_multiple_users(self, driver):
        test_cases = [
            ("user", "user123", True),
            ("test", "test123", True),
            ("user", "wrongpass", False),
            ("nonexistent", "password", False)
        ]
        
        for username, password, should_succeed in test_cases:
            print(f"\nTesting {username}/{password} - should {'succeed' if should_succeed else 'fail'}")
            
            driver.get("http://127.0.0.1:8000/")
            
            username_field = driver.find_element(By.NAME, "username")
            password_field = driver.find_element(By.NAME, "password")
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            login_button.click()
            
            if should_succeed:
                WebDriverWait(driver, 10).until(
                    EC.url_contains("/success")
                )
                assert "/success" in driver.current_url
                print(f"{username} login successful")
                
                driver.find_element(By.CLASS_NAME, "logout").click()
            else:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "error"))
                )
                assert "127.0.0.1:8000/" in driver.current_url
                print(f"{username} login correctly failed")

def test_login_form_elements(driver):
    driver.get("http://127.0.0.1:8000/")
    
    assert driver.find_element(By.NAME, "username").is_displayed()
    assert driver.find_element(By.NAME, "password").is_displayed() 
    assert driver.find_element(By.XPATH, "//button[@type='submit']").is_displayed()
    
    page_text = driver.page_source
    assert "admin / admin123" in page_text
    assert "user / user123" in page_text
    assert "test / test123" in page_text
    
    print("All form elements and test accounts are present")

if __name__ == "__main__":
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        test = TestSimpleAuth()
        test.test_successful_login(driver)
        driver.delete_all_cookies()
        test.test_failed_login(driver)
        driver.delete_all_cookies()
        test.test_multiple_users(driver)
        print("\nALL TESTS PASSED!")
    finally:
        driver.quit()
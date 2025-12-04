import subprocess
import time
import sys

def test_simple():
    """Простой тест для проверки окружения"""
    print("Testing environment...")
    
    # Проверяем доступность Chrome
    try:
        import subprocess
        result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
        print(f"Chrome version: {result.stdout.strip()}")
    except:
        print("Chrome not found")
    
    # Проверяем ChromeDriver
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        print(f"ChromeDriver version: {result.stdout.strip()}")
    except:
        print("ChromeDriver not found")
    
    print("✅ Environment check completed")

if __name__ == "__main__":
    test_simple()
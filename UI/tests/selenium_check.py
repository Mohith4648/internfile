from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys

def test_ui():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get("http://localhost:8080")
        print(f"Page Title: {driver.title}")
        assert driver.title is not None
        print("Build Verified!")
    except Exception as e:
        print(f"Failed: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_ui()

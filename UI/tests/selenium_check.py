from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import sys


def test_ui():
    chrome_options = Options()

    # Headless + CI Optimized Options
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")

    try:
        # Explicitly set ChromeDriver path (works inside Docker)
        service = Service("/usr/bin/chromedriver")

        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )

        target_url = "http://127.0.0.1:8085"
        print(f"Connecting to {target_url}...")

        driver.get(target_url)

        # Smart wait: wait until page title is available (max 10 sec)
        WebDriverWait(driver, 10).until(
            lambda d: d.title and len(d.title) > 0
        )

        print(f"Page Title: {driver.title}")
        print("Build Verified Successfully!")

    except Exception as e:
        print(f"\n❌ SELENIUM TEST FAILED: {e}\n")
        sys.exit(1)

    finally:
        if 'driver' in locals():
            driver.quit()


if __name__ == "__main__":
    test_ui()

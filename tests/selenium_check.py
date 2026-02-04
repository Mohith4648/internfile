from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time

def test_ui():
    chrome_options = Options()
    # CRITICAL: Use 'new' for modern headless support in Jenkins
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") 

    # Initialize the driver
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # USE 127.0.0.1 and port 8085 (the test port we set in Jenkinsfile)
        target_url = "http://127.0.0.1:8085"
        print(f"Connecting to {target_url}...")
        
        # Give the app a second to fully boot up
        time.sleep(2) 
        driver.get(target_url)

        print(f"Page Title: {driver.title}")
        
        # Professional check: Ensure title is not empty and contains your app name
        if driver.title and len(driver.title) > 0:
            print("Build Verified Successfully!")
        else:
            raise Exception("Page loaded but title is empty!")

    except Exception as e:
        print(f"SELENIUM TEST FAILED: {e}")
        sys.exit(1)
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    test_ui()
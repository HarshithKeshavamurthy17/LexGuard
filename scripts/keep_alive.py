import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def keep_alive():
    app_url = os.environ.get("STREAMLIT_APP_URL")
    if not app_url:
        print("Error: STREAMLIT_APP_URL environment variable is not set.")
        return

    print(f"Starting keep-alive check for: {app_url}")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(app_url)
        print("Page loaded.")
        
        # Wait a bit for the page to render
        time.sleep(5)

        # Check for the "Yes, get this app back up!" button
        # The button usually has the text "Yes, get this app back up!"
        try:
            wake_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Yes, get this app back up!')]"))
            )
            print("Wake up button found! Clicking it...")
            wake_button.click()
            print("Clicked wake up button.")
            
            # Wait for the app to restart
            time.sleep(10)
            print("App should be waking up now.")
            
        except Exception as e:
            print("Wake up button not found. The app is likely already awake or the button text is different.")
            # Optional: Print page title or source for debugging if needed
            # print(driver.title)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        print("Driver closed.")

if __name__ == "__main__":
    keep_alive()

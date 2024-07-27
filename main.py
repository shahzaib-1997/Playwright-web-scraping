import undetected_chromedriver as uc
import time, pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def initiate_driver():
    options = uc.ChromeOptions()
    # Disable automation flags
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Disable extensions
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")

    driver = uc.Chrome(options=options)
    driver.maximize_window()
    return driver


def login(driver: webdriver.Chrome, wait: WebDriverWait):
    driver.get("https://www.englandgolf.org/my-golf-login")

    wait.until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Allow all"]'))
    ).click()
    time.sleep(2)

    membership = "1015123002"
    pwd = "Shadow!43"

    membership_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
    )
    membership_input.send_keys(membership)

    pwd_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]'))
    )
    pwd_input.send_keys(pwd)
    pwd_input.send_keys(Keys.ENTER)


def main():
    driver = initiate_driver()
    wait = WebDriverWait(driver, 20)
    login(driver, wait)

    file_path = "2024_07_18-entries (1).csv"

    df = pd.read_csv(file_path)
    driver.quit()


if __name__ == "__main__":
    main()

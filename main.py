import os
import time
import pytz
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By


LOGIN_URL = os.environ.get('LOGIN_URL')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
TIMEZONE = pytz.timezone('Europe/Kiev')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

driver = webdriver.Chrome(
    executable_path=os.environ.get('CHROMEDRIVER_PATH'),
    options=chrome_options)


while True:
    current_time = datetime.now(TIMEZONE)
    start_time = current_time.replace(hour=18, minute=0, second=0, microsecond=0)
    end_time = current_time.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)

    if start_time <= current_time <= end_time:
        try:
            # Открыть страницу для авторизации
            driver.get(LOGIN_URL)
            time.sleep(3)

            # Найти элементы для ввода логина и пароля с использованием метода By.XPATH
            login_input = driver.find_element(
                By.XPATH,
                '//*[@id="body"]/div/div[1]/div/div[1]/div[2]/div[1]/div/input'
            )
            password_input = driver.find_element(
                By.XPATH,
                '//*[@id="body"]/div/div[1]/div/div[2]/div/div[2]/div[1]/div/input'
            )

            # Ввести логин и пароль
            login_input.send_keys(USERNAME)
            password_input.send_keys(PASSWORD)

            # Найти и нажать кнопку "Войти"
            login_button = driver.find_element(
                By.XPATH,
                '//*[@id="body"]/div/div[1]/div/div[8]/div/div/div/div/span')
            login_button.click()

            # Ждем 15 минут
            time.sleep(910)
            driver.close()

        except Exception as e:
            print("Ошибка:", e)

        finally:
            driver.quit()

    else:
        continue

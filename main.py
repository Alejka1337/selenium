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
CHROMEDRIVER_PATH = os.environ.get('CHROMEDRIVER_PATH')

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--chromedriver-executable={CHROMEDRIVER_PATH}')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")


while True:
    current_time = datetime.now(TIMEZONE)
    day_of_week = current_time.weekday()  # 0 for Monday, 6 for Sunday

    # Проверяем, если сейчас пятница
    if day_of_week == 4:
        # Если сейчас пятница, ждем до 18:00
        if current_time.hour < 18:
            time_to_wait = datetime(current_time.year, current_time.month, current_time.day, 18, 0, 0) - current_time
            time.sleep(time_to_wait.total_seconds())
    else:
        # Если не пятница, ждем до 18:00
        if current_time.hour < 18:
            time_to_wait = datetime(current_time.year, current_time.month, current_time.day, 18, 0, 0) - current_time
            time.sleep(time_to_wait.total_seconds())

    while (day_of_week < 5 and current_time.hour >= 18) or \
            (day_of_week == 4 and current_time.hour >= 18):
        print(f'Пробую авторизироваться {datetime.now()}')
        driver = webdriver.Chrome(options=chrome_options)

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
        time.sleep(10)
        print(f'Поспал {datetime.now()}')
        continue

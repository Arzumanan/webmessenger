import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from config import URL, LOGIN_ADMIN, PASSWORD_ADMIN

def test_open_website():
    driver = webdriver.Chrome()
    try:
        # Открытие сайта
        driver.get(URL)
        assert "Веб-мессенджер" in driver.title

        # Нажатие кнопки входа (с явным ожиданием и прокруткой)
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[2]/div[1]/button[1]'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
            print("✅ Кнопка входа успешно нажата")
        except (TimeoutException, ElementNotInteractableException) as e:
            print(f"❌ Ошибка при нажатии кнопки: {str(e)}")
            driver.save_screenshot("button_error.png")
            raise

        # Ввод учетных данных
        try:
            # Ожидание и ввод email
            email_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))
            )
            email_field.clear()
            email_field.send_keys(LOGIN_ADMIN)

            # Ожидание и ввод пароля
            password_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
            )
            password_field.clear()
            password_field.send_keys(PASSWORD_ADMIN)

            # Клик по кнопке входа
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/form/div[3]/div/button[2]'))
            )
            login_button.click()
            print("✅ Данные для входа отправлены")
        except Exception as e:
            print(f"❌ Ошибка при вводе учетных данных: {str(e)}")
            driver.save_screenshot("login_error.png")
            raise

        # Проверка успешной авторизации
        try:
            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div/span'))
            )
            print("✅ Авторизация успешна: элемент 'Диалог' найден")
        except TimeoutException:
            print("❌ Элемент 'Диалог' не найден после авторизации")
            driver.save_screenshot("auth_failed.png")
            raise

    finally:
        driver.quit()

if __name__ == "__main__":
    test_open_website()
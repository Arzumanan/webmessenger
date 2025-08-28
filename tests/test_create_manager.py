import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from config.data import admin_email, admin_password
from config.links import Links
from pages.managers_page import ManagersPage


def create_chrome():
    options = webdriver.ChromeOptions()
    # Отключить системные запросы на показ уведомлений
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    return webdriver.Chrome(options=options)

def test_open_website():
    driver = create_chrome()
    try:
        # Открытие сайта
        driver.get(Links.HOST)
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
            email_field.send_keys(admin_email)

            # Ожидание и ввод пароля
            password_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
            )
            password_field.clear()
            password_field.send_keys(admin_password)

            # Делаем кнопку активной и ждём, пока пропадёт disabled
            login_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/form/div[3]/div/button[2] | //button[contains(.,"Войти")]'))
            )
            WebDriverWait(driver, 10).until(lambda d: login_button.get_attribute("disabled") in (None, "false"))
            # Дополнительно жмём Enter по паролю на случай перехвата формой
            password_field.send_keys("\n")
            try:
                WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div/form/div[3]/div/button[2] | //button[contains(.,"Войти")]'))).click()
            except Exception:
                pass
            print("✅ Данные для входа отправлены")
        except Exception as e:
            print(f"❌ Ошибка при вводе учетных данных: {str(e)}")
            driver.save_screenshot("login_error.png")
            raise

        # Проверка успешной авторизации
        try:
            WebDriverWait(driver, 20).until(lambda d: '/login' not in d.current_url)
            WebDriverWait(driver, 20).until(
                EC.any_of(
                    EC.visibility_of_element_located((By.XPATH, '//*[contains(@class,"navbar") or contains(@class,"messenger")]')),
                    EC.visibility_of_element_located((By.XPATH, '//*[text()="Диалоги" or contains(@class,"navlink-text")]')),
                )
            )
            print("✅ Авторизация успешна: элемент 'Диалог' найден")
        except TimeoutException:
            print(f"❌ После авторизации остались на странице: {driver.current_url}")
            driver.save_screenshot("auth_failed.png")
            raise

        # Переход в раздел Менеджеры по <a id="managers">
        try:
            managers_sidebar_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "managers"))
            )
            managers_sidebar_btn.click()
            print("✅ Перешли в раздел 'Менеджеры' по <a id='managers'>")
            time.sleep(2)
            # Клик по кнопке 'Добавить менеджера'
            add_manager_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'manager-sidebar-add-manager-btn') and contains(text(),'Добавить менеджера')]"))
            )
            add_manager_btn.click()
            print("✅ Кнопка 'Добавить менеджера' нажата")
            # Ждем появления модального окна добавления менеджера и заполняем поля рандомными данными
            modal_title = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'modal__title') and text()='Добавление менеджера']"))
            )
            print("✅ Окно добавления менеджера открыто")

            import random, string
            def random_string(length=8):
                return ''.join(random.choices(string.ascii_letters, k=length))
            def random_email():
                return random_string(6) + "@test.com"
            name = random_string(6)
            email = random_email()
            password = random_string(10)

            # Используем Page Object для заполнения и сабмита
            managers_page = ManagersPage(driver)
            managers_page.add_manager(name=name, email=email, password=password)

            # Проверяем, что менеджер появился в списке
            created_manager = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{email}')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", created_manager)
            print("✅ Менеджер создан и отображается в списке:", email)

            # Удаляем созданного менеджера через Page Object
            managers_page.delete_manager(email)
            print("✅ Менеджер удалён:", email)

        except Exception as e:
            print(f"❌ Не удалось перейти в раздел 'Менеджеры': {str(e)}")
            driver.save_screenshot("sidebar_error.png")
            raise

        # Попытка закрыть возможный внутрисайтовый баннер с просьбой разрешить уведомления
        try:
            deny = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((
                By.XPATH,
                '//*[self::button or self::a][contains(., "Не сейчас") or contains(., "Позже") or contains(., "Запретить") or contains(., "Не разрешать") or contains(., "Закрыть")]'
            )))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", deny)
            time.sleep(0.3)
            try:
                deny.click()
            except Exception:
                driver.execute_script("arguments[0].click();", deny)
        except Exception:
            # Альтернатива: закрытие по иконке крестика
            try:
                close_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[contains(@class, "close") or contains(@class, "icon-close")][self::button or self::span or self::i]'
                )))
                try:
                    close_btn.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", close_btn)
            except Exception:
                pass

    finally:
        driver.quit()

if __name__ == "__main__":
    test_open_website()
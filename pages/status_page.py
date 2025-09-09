import allure
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class StatusPage(BasePage):
    PAGE_URL = "https://testim.i2crm.ru/tags-statuses"

    # Локаторы для кнопок и полей добавления статуса
    ADD_STATUS_BUTTON = ("xpath", "//button[contains(@class, 'tags-status-settings__add-btn') and contains(text(), '+ Добавить статус')]")
    STATUS_INPUT_FIELD = ("xpath", "//input[@class='add-contact-form-control-input' and @placeholder='Текст']")
    SUBMIT_ADD_STATUS_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and contains(text(), 'Добавить статус')]")
    
    # Локаторы для выбора цвета статуса
    COLOR_BUTTONS = ("xpath", "//button[contains(@class, 'add-contact-form-color-item') and not(contains(@class, 'others'))]")
    
    # Локаторы для модального окна
    MODAL_HEADER = ("xpath", "//div[@class='add-contact-header-text' and text()='Добавить статус']")

    @allure.step("Открытие страницы статусов")
    def open_status_page(self):
        """Открытие страницы статусов"""
        self.browser.get(self.PAGE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    @allure.step("Нажатие на кнопку 'Добавить статус'")
    def click_add_status_button(self):
        """Нажатие на кнопку добавления статуса"""
        add_button = self.element_in_clickable(self.ADD_STATUS_BUTTON)
        add_button.click()

    @allure.step("Заполнение поля ввода статуса")
    def fill_status_input(self, status_text):
        """Заполнение поля ввода статуса"""
        status_input = self.element_in_clickable(self.STATUS_INPUT_FIELD)
        status_input.clear()
        status_input.send_keys(status_text)

    @allure.step("Выбор цвета статуса")
    def select_status_color(self, color_index=None):
        """Выбор цвета статуса по индексу (0-4) или случайный"""
        if color_index is None:
            color_index = random.randint(0, 4)
        
        color_buttons = self.elements_in_visible(self.COLOR_BUTTONS)
        if color_index < len(color_buttons):
            color_buttons[color_index].click()
            return color_index
        else:
            # Если индекс выходит за границы, выбираем первый доступный цвет
            color_buttons[0].click()
            return 0

    @allure.step("Нажатие на кнопку 'Добавить статус' для сохранения")
    def click_submit_add_status(self):
        """Нажатие на кнопку сохранения статуса"""
        submit_button = self.element_in_clickable(self.SUBMIT_ADD_STATUS_BUTTON)
        submit_button.click()

    @allure.step("Создание нового статуса")
    def create_status(self, status_text, color_index=None):
        """Полный процесс создания статуса"""
        self.click_add_status_button()
        
        # Ждем появления модального окна
        self.element_in_visible(self.MODAL_HEADER)
        
        self.fill_status_input(status_text)
        self.select_status_color(color_index)
        self.click_submit_add_status()
        
        # Ждем, пока статус появится на странице
        import time
        time.sleep(2)  # Даем время на обновление страницы

    @allure.step("Генерация случайного статуса")
    def generate_random_status(self, min_length=4, max_length=19):
        """Генерация случайного статуса заданной длины (максимум 19 символов)"""
        length = random.randint(min_length, min(max_length, 19))
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @allure.step("Поиск статуса по тексту")
    def find_status_by_text(self, status_text):
        """Поиск статуса по тексту"""
        # Ищем по точной структуре HTML
        locators = [
            f"//span[@class='status-item_title' and text()='{status_text}']",
            f"//span[@class='status-item_title' and contains(text(), '{status_text}')]",
            f"//li[@class='status-item']//span[@class='status-item_title' and text()='{status_text}']",
            f"//li[@class='status-item']//span[@class='status-item_title' and contains(text(), '{status_text}')]"
        ]
        
        for xpath in locators:
            try:
                elements = self.browser.find_elements(By.XPATH, xpath)
                if elements:
                    return elements[0]
            except:
                continue
        
        return None

    @allure.step("Проверка наличия статуса")
    def is_status_present(self, status_text):
        """Проверка наличия статуса на странице"""
        status_element = self.find_status_by_text(status_text)
        return status_element is not None


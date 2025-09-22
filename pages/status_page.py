import allure
import random
import string
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class StatusPage(BasePage):
    PAGE_URL = "https://testim.i2crm.ru/tags-statuses"

    # Константы
    MIN_STATUS_LENGTH = 4
    MAX_STATUS_LENGTH = 19

    # Локаторы
    ADD_STATUS_BUTTON = ("xpath", "//button[contains(@class, 'tags-status-settings__add-btn') and contains(text(), '+ Добавить статус')]")
    STATUS_INPUT_FIELD = ("xpath", "//input[@class='add-contact-form-control-input' and @placeholder='Текст']")
    SUBMIT_ADD_STATUS_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and contains(text(), 'Добавить статус')]")
    CONFIRM_DELETE_YES_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and text()='Да']")
    CONFIRM_EDIT_BUTTON = ("xpath", "//div[@class='warning_wrapper']//button[contains(text(), 'Да')]")
    EDIT_STATUS_INPUT = ("xpath", "//input[@class='add-contact-form-control-input']")
    SAVE_EDIT_BUTTON = ("xpath", "//button[@type='button' and text()='Сохранить']")
    ERROR_SHORT_STATUS = ("xpath", "//span[@class='add-contact-form-control-label-red' and text()='Введите более 3 символов.']")
    ERROR_COLOR_STATUS = ("xpath", "//span[@class='add-contact-form-control-label-red' and text()='Все поля обязательны для заполнения.']")
    
    # Локаторы для выбора цвета статуса
    COLOR_BUTTONS = ("xpath", "//button[contains(@class, 'add-contact-form-color-item') and not(contains(@class, 'others'))]")
    
    # Локаторы для модального окна
    MODAL_HEADER = ("xpath", "//div[@class='add-contact-header-text' and text()='Добавить статус']")

    # Динамические локаторы
    @staticmethod
    def get_status_locator(status_text):
        """Локатор для поиска статуса по тексту"""
        return ("xpath", f"//span[@class='status-item_title' and text()='{status_text}']")
    
    @staticmethod
    def get_delete_status_locator(status_text):
        """Локатор для кнопки удаления статуса"""
        return ("xpath", f"//span[@class='status-item_title' and text()='{status_text}']/following-sibling::*[name()='svg'][2]")
    
    @staticmethod
    def get_edit_status_locator(status_text):
        """Локатор для кнопки редактирования статуса"""
        return ("xpath", f"//span[@class='status-item_title' and text()='{status_text}']/following-sibling::*[name()='svg'][1]")

    # Основные действия
    @allure.step("Открытие страницы статусов")
    def open_status_page(self):
        self.browser.get(self.PAGE_URL)
        self.element_in_visible((By.TAG_NAME, "body"))

    @allure.step("Нажатие на кнопку добавления статуса")
    def click_add_status_button(self):
        self.element_in_clickable(self.ADD_STATUS_BUTTON).click()

    @allure.step("Ввод текста в поле статуса")
    def input_status_field(self, status_text):
        self.element_in_clickable(self.STATUS_INPUT_FIELD).send_keys(status_text)

    @allure.step("Выбор цвета статуса")
    def select_status_color(self, color_index=None):
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

    @allure.step("Нажатие на кнопку сохранения статуса")
    def click_submit_add_status_button(self):
        self.element_in_clickable(self.SUBMIT_ADD_STATUS_BUTTON).click()

    @allure.step("Создание статуса")
    def create_status(self, status_text=None, color_index=None):
        """Создание нового статуса с автоматическим трекингом"""
        if status_text is None:
            status_text = self.generate_random_status()

        # Создание статуса
        self.element_in_clickable(self.ADD_STATUS_BUTTON).click()
        
        # Ждем появления модального окна
        self.element_in_visible(self.MODAL_HEADER)
        
        status_input = self.element_in_clickable(self.STATUS_INPUT_FIELD)
        status_input.clear()
        status_input.send_keys(status_text)
        
        self.select_status_color(color_index)
        self.element_in_clickable(self.SUBMIT_ADD_STATUS_BUTTON).click()
        return status_text

    @allure.step("Удаление статуса")
    def delete_status(self, status_text):
        """Удаление статуса по названию"""
        delete_locator = self.get_delete_status_locator(status_text)
        self.element_in_clickable(delete_locator).click()
        self.element_in_clickable(self.CONFIRM_DELETE_YES_BUTTON).click()

    @allure.step("Редактирование статуса")
    def edit_status(self, old_status_text, new_status_text, color_index=None):
        """Редактирование существующего статуса"""
        edit_locator = self.get_edit_status_locator(old_status_text)
        self.element_in_clickable(edit_locator).click()

        # Подтверждение и редактирование
        self.element_in_clickable(self.CONFIRM_EDIT_BUTTON).click()

        edit_input = self.element_in_clickable(self.EDIT_STATUS_INPUT)
        edit_input.clear()
        edit_input.send_keys(new_status_text)

        # Выбор цвета при редактировании (если указан)
        if color_index is not None:
            self.select_status_color(color_index)

        self.element_in_clickable(self.SAVE_EDIT_BUTTON).click()
        return new_status_text

    # Проверки
    @allure.step("Проверка наличия статуса")
    def is_status_present(self, status_text):
        try:
            status_locator = self.get_status_locator(status_text)
            self.element_in_visible(status_locator)
            assert True, f"Статус '{status_text}' найден на странице"
        except Exception as e:
            assert False, f"Статус '{status_text}' не найден на странице. Ошибка: {str(e)}"

    @allure.step("Проверка отсутствия статуса")
    def is_status_not_present(self, status_text):
        try:
            status_locator = self.get_status_locator(status_text)
            self.element_is_not_visible(status_locator)
            assert True, f"Статус '{status_text}' отсутствует на странице"
        except Exception as e:
            assert False, f"Статус '{status_text}' все еще присутствует на странице. Ошибка: {str(e)}"

    @allure.step("Проверка ошибки короткого статуса")
    def check_error_short_status(self):
        """Проверка отображения ошибки для короткого статуса"""
        try:
            self.element_in_visible(self.ERROR_SHORT_STATUS)
            assert True, "Ошибка короткого статуса отображается корректно"
        except Exception as e:
            assert False, f"Ошибка короткого статуса не отображается. Ошибка: {str(e)}"

    @allure.step("Проверка ошибки цвета статуса")
    def check_error_color_status(self):
        """Проверка отображения ошибки для цвета статуса"""
        try:
            self.element_in_visible(self.ERROR_COLOR_STATUS)
            assert True, "Ошибка цвета статуса отображается корректно"
        except Exception as e:
            assert False, f"Ошибка цвета статуса не отображается. Ошибка: {str(e)}"

    # Утилиты
    @allure.step("Генерация случайного статуса")
    def generate_random_status(self, min_length=None, max_length=None):
        """Генерация случайного статуса"""
        min_len = min_length or self.MIN_STATUS_LENGTH
        max_len = max_length or self.MAX_STATUS_LENGTH
        length = random.randint(min_len, max_len)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



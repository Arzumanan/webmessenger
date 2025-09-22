import allure
import random
import string
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class TagsPage(BasePage):
    PAGE_URL = "https://testim.i2crm.ru/tags-statuses"

    # Константы
    MIN_TAG_LENGTH = 4
    MAX_TAG_LENGTH = 17

    # Локаторы
    ADD_TAG_BUTTON = ("xpath", "//button[contains(@class, 'tags-status-settings__add-btn') and contains(text(), '+ Добавить тег')]")
    TAG_INPUT_FIELD = ("xpath", "//input[@class='add-contact-form-control-input' and @placeholder='Текст']")
    SUBMIT_ADD_TAG_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and contains(text(), 'Добавить тег')]")
    CONFIRM_DELETE_YES_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and text()='Да']")
    CONFIRM_EDIT_BUTTON = ("xpath", "//div[@class='warning_wrapper']//button[contains(text(), 'Да')]")
    EDIT_TAG_INPUT = ("xpath", "//input[@class='add-contact-form-control-input']")
    SAVE_EDIT_BUTTON = ("xpath", "//button[@type='button' and text()='Сохранить']")
    ERROR_SHORT_TAG = ("xpath", "//span[@class='add-contact-form-control-label-red' and text()='Введите более 3 символов.']")


    # Динамические локаторы
    @staticmethod
    def get_tag_locator(tag_text):
        """Локатор для поиска тега по тексту"""
        return ("xpath", f"//span[@class='tag-item_title' and text()='{tag_text}']")

    @staticmethod
    def get_delete_tag_locator(tag_text):
        """Локатор для кнопки удаления тега"""
        return ("xpath", f"//span[@class='tag-item_title' and text()='{tag_text}']/following-sibling::*[name()='svg'][2]")

    @staticmethod
    def get_edit_tag_locator(tag_text):
        """Локатор для кнопки редактирования тега"""
        return ("xpath", f"//span[@class='tag-item_title' and text()='{tag_text}']/following-sibling::*[name()='svg'][1]")

    # Основные действия
    @allure.step("Открытие страницы тегов")
    def open_tags_page(self):
        """Открытие страницы управления тегами"""
        self.browser.get(self.PAGE_URL)
        self.element_in_visible((By.TAG_NAME, "body"))

    @allure.step("Нажатие на кнопку добавления тега")
    def click_add_tag_button(self):
        """Нажатие на кнопку добавления тега"""
        self.element_in_clickable(self.ADD_TAG_BUTTON).click()

    @allure.step("Ввод текста в поле тега")
    def input_tag_field(self, tag_text):
        """Ввод текста в поле тега"""
        self.element_in_clickable(self.TAG_INPUT_FIELD).send_keys(tag_text)

    @allure.step("Нажатие на кнопку сохранения тега")
    def click_submit_add_tag_button(self):
        """Нажатие на кнопку сохранения тега"""
        self.element_in_clickable(self.SUBMIT_ADD_TAG_BUTTON).click()

    @allure.step("Создание тега")
    def create_tag(self, tag_text=None):
        """Создание нового тега с автоматическим трекингом"""
        if tag_text is None:
            tag_text = self.generate_random_tag()

        # Создание тега
        self.element_in_clickable(self.ADD_TAG_BUTTON).click()

        tag_input = self.element_in_clickable(self.TAG_INPUT_FIELD)
        tag_input.clear()
        tag_input.send_keys(tag_text)

        self.element_in_clickable(self.SUBMIT_ADD_TAG_BUTTON).click()
        return tag_text

    @allure.step("Удаление тега")
    def delete_tag(self, tag_text):
        """Удаление тега по названию"""
        delete_locator = self.get_delete_tag_locator(tag_text)
        self.element_in_clickable(delete_locator).click()
        self.element_in_clickable(self.CONFIRM_DELETE_YES_BUTTON).click()

    @allure.step("Редактирование тега")
    def edit_tag(self, old_tag_text, new_tag_text):
        """Редактирование существующего тега"""
        edit_locator = self.get_edit_tag_locator(old_tag_text)
        self.element_in_clickable(edit_locator).click()

        # Подтверждение и редактирование
        self.element_in_clickable(self.CONFIRM_EDIT_BUTTON).click()

        edit_input = self.element_in_clickable(self.EDIT_TAG_INPUT)
        edit_input.clear()
        edit_input.send_keys(new_tag_text)

        self.element_in_clickable(self.SAVE_EDIT_BUTTON).click()
        return new_tag_text

    # Проверки
    @allure.step("Проверка наличия тега")
    def is_tag_present(self, tag_text):
        """Проверка наличия тега на странице"""
        try:
            tag_locator = self.get_tag_locator(tag_text)
            self.element_in_visible(tag_locator)
            assert True, f"Тег '{tag_text}' найден на странице"
        except Exception as e:
            assert False, f"Тег '{tag_text}' не найден на странице. Ошибка: {str(e)}"

    @allure.step("Проверка отсутствия тега")
    def is_tag_not_present(self, tag_text):
        """Проверка отсутствия тега на странице"""
        try:
            tag_locator = self.get_tag_locator(tag_text)
            self.element_is_not_visible(tag_locator)
            assert True, f"Тег '{tag_text}' отсутствует на странице"
        except Exception as e:
            assert False, f"Тег '{tag_text}' все еще присутствует на странице. Ошибка: {str(e)}"

    @allure.step("Проверка ошибки короткого тега")
    def check_error_short_tag(self):
        """Проверка отображения ошибки для короткого тега"""
        try:
            self.element_in_visible(self.ERROR_SHORT_TAG)
            assert True, "Ошибка короткого тега отображается корректно"
        except Exception as e:
            assert False, f"Ошибка короткого тега не отображается. Ошибка: {str(e)}"

    # Утилиты
    @allure.step("Генерация случайного тега")
    def generate_random_tag(self, min_length=None, max_length=None):
        """Генерация случайного тега"""
        min_len = min_length or self.MIN_TAG_LENGTH
        max_len = max_length or self.MAX_TAG_LENGTH
        length = random.randint(min_len, max_len)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
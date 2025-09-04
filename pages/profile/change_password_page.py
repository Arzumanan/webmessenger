"""
Страница смены пароля профиля
"""
from time import sleep
import allure
from pages.base_page import BasePage


class ChangePasswordPage(BasePage):
    """Класс для работы со страницей смены пароля"""
    
    # Локаторы элементов страницы
    CURRENT_PASSWORD_FIELD = ("xpath", "//input[@id='oldPassword']")
    NEW_PASSWORD_FIELD = ("xpath", "//input[@id='password']")
    CONFIRM_PASSWORD_FIELD = ("xpath", "//input[@id='repeatPassword']")
    SAVE_BUTTON = ("xpath", "//button[@type='submit' and contains(text(), 'Сохранить')]")
    CANCEL_BUTTON = ("xpath", "//button[contains(text(), 'Отмена')]")
    SUCCESS_MESSAGE = ("xpath", "//div[contains(@class, 'success-message')]")
    ERROR_MESSAGE = ("xpath", "//p[contains(@class, 'form-status')]")
    ERROR_MESSAGE2 = ("xpath", "//label[contains(@class, 'input__label') and contains(text(),'Пароли должны совпадать')]")
    PASSWORD_STRENGTH_INDICATOR = ("xpath", "//div[contains(@class, 'password-strength')]")
    PROFILE_CHANGE_PASSWORD_BUTTON = ("xpath", "//button[contains(text(), 'Сменить пароль')]")
    PROFILE_BUTTON = ("xpath", "//span[contains(text(), 'Профиль')]")
    RAZV_BUTTON = ("xpath", "//button[contains(@class, 'navbar-toggle')]")
    
    @allure.step('Открытие страницы смены пароля')
    def open_change_password_page(self):
        """Открыть страницу смены пароля"""
        self.element_in_clickable(self.RAZV_BUTTON).click()
        self.element_in_clickable(self.PROFILE_BUTTON).click()
        self.element_in_clickable(self.PROFILE_CHANGE_PASSWORD_BUTTON).click()
        sleep(2)
       


    @allure.step('Сохранение пустой формы')
    def save_empty_password(self, password):
        """Не вводить пароль"""
        self.element_in_clickable(self.SAVE_BUTTON).click()
        sleep(2)
    
    @allure.step('Ввод текущего пароля')
    def enter_current_password(self, password):
        """Ввести текущий пароль"""
        self.element_in_localed(self.CURRENT_PASSWORD_FIELD).clear()
        self.element_in_localed(self.CURRENT_PASSWORD_FIELD).send_keys(password)
        return self
    
    @allure.step('Ввод нового пароля')
    def enter_new_password(self, password):
        """Ввести новый пароль"""
        self.element_in_localed(self.NEW_PASSWORD_FIELD).clear()
        self.element_in_localed(self.NEW_PASSWORD_FIELD).send_keys(password)
        return self
    
    @allure.step('Подтверждение нового пароля')
    def enter_confirm_password(self, password):
        """Подтвердить новый пароль"""
        self.element_in_localed(self.CONFIRM_PASSWORD_FIELD).clear()
        self.element_in_localed(self.CONFIRM_PASSWORD_FIELD).send_keys(password)
        return self
    
    @allure.step('Нажатие кнопки сохранения')
    def click_save_button(self):
        """Нажать кнопку сохранения"""
        self.element_in_clickable(self.SAVE_BUTTON).click()
        return self
    
    @allure.step('Нажатие кнопки отмены')
    def click_cancel_button(self):
        """Нажать кнопку отмены"""
        self.element_in_clickable(self.CANCEL_BUTTON).click()
        return self
    
    @allure.step('Полный процесс смены пароля')
    def change_password(self, current_password, new_password, confirm_password=None):
        """Полный процесс смены пароля"""
        if confirm_password is None:
            confirm_password = new_password
            
        self.enter_current_password(current_password)
        self.enter_new_password(new_password)
        self.enter_confirm_password(confirm_password)
        self.click_save_button()
        return self
    
    def is_success_message_displayed(self):
        """Проверить, отображается ли сообщение об успехе"""
        try:
            success_message = self.element_in_visible(self.SUCCESS_MESSAGE, timeout=5)
            return success_message.is_displayed()
        except:
            return False
    
    def is_error_message_displayed(self):
        """Проверить, отображается ли сообщение об ошибке"""
        try:
            error_message = self.element_in_visible(self.ERROR_MESSAGE, timeout=5)
            return error_message.is_displayed()
        except:
            return False
    
    def get_success_message_text(self):
        """Получить текст сообщения об успехе"""
        try:
            success_message = self.element_in_visible(self.SUCCESS_MESSAGE, timeout=5)
            return success_message.text
        except:
            return ""
    
    def get_error_message_text(self):
        """Получить текст сообщения об ошибке"""
        try:
            error_message = self.element_in_visible(self.ERROR_MESSAGE, timeout=5)
            return error_message.text
        except:
            return ""

    def get_error_message_text2(self):
        """Получить текст сообщения об ошибке2"""
        try:
            error_message = self.element_in_visible(self.ERROR_MESSAGE2, timeout=5)
            return error_message.text
        except:
            return ""        
    
    def get_password_strength(self):
        """Получить индикатор силы пароля"""
        try:
            strength_indicator = self.find_element(self.PASSWORD_STRENGTH_INDICATOR)
            return strength_indicator.text
        except:
            return ""
    
    def is_save_button_enabled(self):
        """Проверить, активна ли кнопка сохранения"""
        try:
            save_button = self.find_element(self.SAVE_BUTTON)
            return save_button.is_enabled()
        except:
            return False
    
    @allure.step('Очистка всех полей формы')
    def clear_all_fields(self):
        """Очистить все поля формы"""
        self.enter_current_password("")
        self.enter_new_password("")
        self.enter_confirm_password("")
        return self

"""
Страница смены пароля пользователя
"""
import allure
from pages.base_page import BasePage


class ChangePasswordPage(BasePage):
    """Класс для работы со страницей смены пароля"""
    
    # Локаторы элементов страницы
    CURRENT_PASSWORD_FIELD = ("xpath", "//input[@id='current-password']")
    NEW_PASSWORD_FIELD = ("xpath", "//input[@id='new-password']")
    CONFIRM_PASSWORD_FIELD = ("xpath", "//input[@id='confirm-password']")
    SAVE_BUTTON = ("xpath", "//button[@type='submit' and contains(text(), 'Сохранить')]")
    CANCEL_BUTTON = ("xpath", "//button[contains(text(), 'Отмена')]")
    SUCCESS_MESSAGE = ("xpath", "//div[contains(@class, 'success-message')]")
    ERROR_MESSAGE = ("xpath", "//div[contains(@class, 'error-message')]")
    PASSWORD_STRENGTH_INDICATOR = ("xpath", "//div[contains(@class, 'password-strength')]")
    
    @allure.step('Открытие страницы смены пароля')
    def open_change_password_page(self):
        """Открыть страницу смены пароля"""
        # Здесь должен быть URL или переход к странице смены пароля
        # self.browser.get(f"{self.base_url}/profile/change-password")
        pass
    
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

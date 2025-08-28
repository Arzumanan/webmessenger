import allure
from selenium.webdriver.common.by import By

from config.links import Links
from pages.base_page import BasePage


class LoginAdminPage(BasePage):
    PAGE_URL = Links.HOST
    ADMIN_LOGIN_URL = Links.ADMIN_LOGIN_URL
    ADMIN_LOGIN_BUTTON = ("xpath", "//button[contains(text(),'Администратор')]")
    EMAIL_INPUT = ("xpath", "//input[@id = 'email']")
    PASSWORD_INPUT = ("xpath", "//input[@id = 'password']")
    LOGIN_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and contains(text(),'Войти')]")
    DIALOGS_SIDEBAR = ("xpath", "//span[@class='sidebar-header-profile-name' and text()='Диалоги']")

    @allure.step('Переход на страницу авторизации администратора')
    def open_admin_login_page(self):
        self.element_in_clickable(self.ADMIN_LOGIN_BUTTON).click()

    @allure.step('Ввод email')
    def enter_email(self, email):
        self.element_in_localed(self.EMAIL_INPUT).send_keys(email)

    @allure.step('Ввод password')
    def enter_password(self, password):
        self.element_in_localed(self.PASSWORD_INPUT).send_keys(password)

    @allure.step('Нажатие на кнопку авторизации')
    def admin_authorization(self):
        self.element_in_clickable(self.LOGIN_BUTTON).click()

    @allure.step('Проверка результата авторизации')
    def check_authorization(self, expected_result, expected_error_message):
        if expected_result:
            self.element_in_visible(self.DIALOGS_SIDEBAR).is_displayed()
            assert self.browser.current_url != self.ADMIN_LOGIN_URL

        else:
            error_locator = (By.XPATH, f"//*[text() = '{expected_error_message}']")
            self.element_in_visible(error_locator)
            assert self.element_in_visible(error_locator).is_displayed()
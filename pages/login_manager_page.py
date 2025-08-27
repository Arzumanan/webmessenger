from time import sleep

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Импорт WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.links import Links
from pages.base_page import BasePage


class LoginManagerPage(BasePage):


    PAGE_URL = Links.HOST
    MANAGER_LOGIN_URL = Links.MANAGER_LOGIN_URL

    MANAGER_LOGIN_BUTTON = ("xpath", "//button[contains(text(), 'Менеджер')]")
    EMAIL_INPUT = ("xpath", "//input[@id = 'email']")
    PASSWORD_INPUT = ("xpath", "//input[@id = 'password']")
    LOGIN_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and contains(text(),'Войти')]")
    DIALOGS_SIDEBAR = ("xpath", "//span[@class='sidebar-header-profile-name' and text()='Диалоги']")



    @allure.step('Переход на страницу авторизации менеджера')
    def open_manager_login_page(self):
        self.element_in_clickable(self.MANAGER_LOGIN_BUTTON).click()

    @allure.step('Ввод email')
    def enter_email(self, email):
        self.element_in_localed(self.EMAIL_INPUT).send_keys(email)

    @allure.step('Ввод password')
    def enter_password(self, password):
        self.element_in_localed(self.PASSWORD_INPUT).send_keys(password)

    @allure.step('Нажатие на кнопку авторизации')
    def manager_authorization(self):
        self.element_in_clickable(self.LOGIN_BUTTON).click()

    @allure.step('Нажатие на кнопку авторизации')
    def check_authorization(self, expected_result, expected_error_message):
        if expected_result:
            self.element_in_visible(self.DIALOGS_SIDEBAR).is_displayed()
            assert self.browser.current_url != self.MANAGER_LOGIN_URL

        else:
            error_locator = (By.XPATH, f"//*[text() = '{expected_error_message}']")
            self.element_in_visible(error_locator)
            assert self.element_in_visible(error_locator).is_displayed()

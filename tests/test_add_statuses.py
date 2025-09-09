import allure
import pytest
import random
from config.data import admin_email, admin_password
from pages.base_test import BaseTest


@allure.suite("Создание статуса")
class TestAddStatus(BaseTest):

    @allure.title("Создание статуса")
    def test_add_status(self):
        self.base_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()
        
        self.login_admin_page.check_authorization(True, None)
        
        self.status_page.open_status_page()
        
        # Генерируем случайный статус
        test_status = self.status_page.generate_random_status(4, 19)
        
        with allure.step("Создание нового статуса"):
            self.status_page.create_status(test_status, 2)
            
        with allure.step("Проверка создания статуса"):
            assert self.status_page.is_status_present(test_status), \
                f"Статус '{test_status}' не был создан"
import allure
import pytest

from config.data import admin_email, admin_password, invalid_email, invalid_password, short_password
from pages.base_test import BaseTest


@allure.suite("Авторизация администратора с разными данными")
@pytest.mark.parametrize(
    "email, password, expected_result, expected_error_message",
    [
        pytest.param(admin_email, admin_password, True, None,
                     id="Authorization"),
        pytest.param(admin_email, invalid_password, False, "Неверный логин или пароль.",
                     id="ERROR Authorization"),
        pytest.param(invalid_email, admin_password, False, "Пожалуйста, введите корректный email-адрес",
                     id="ERROR Email"),
        pytest.param(admin_email, short_password, False, "Пароль должен содержать не менее 8 символов",
                     id="ERROR password"),
    ],
)
class TestAdminLogin(BaseTest):

    @allure.title("Авторизация администратора")
    def test_login_admin(self, email, password, expected_result, expected_error_message):
        self.base_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(email)
        self.login_admin_page.enter_password(password)
        self.login_admin_page.admin_authorization()
        self.login_admin_page.check_authorization(expected_result, expected_error_message)

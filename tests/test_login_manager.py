import allure
import pytest
from config.data import manager_email, manager_password, invalid_email, invalid_password, short_password
from pages.base_test import BaseTest


@allure.suite("Авторизация менеджера с разными данными")
@pytest.mark.parametrize(
    "email, password, expected_result, expected_error_message",
    [
        pytest.param(manager_email, manager_password, True, None,
                     id="Authorization"),
        pytest.param(manager_email, invalid_password, False, "Неверный логин или пароль.",
                     id="ERROR Authorization"),
        pytest.param(invalid_email, manager_password, False, "Пожалуйста, введите корректный email-адрес",
                     id="ERROR Email"),
        pytest.param(manager_email, short_password, False, "Пароль должен содержать не менее 8 символов",
                     id="ERROR password"),
    ],
)
class TestManagerLogin(BaseTest):

    @allure.title("Авторизация менеджера")
    def test_login_manager(self, email, password, expected_result, expected_error_message):
        self.base_page.open_host()
        self.login_manager_page.open_manager_login_page()
        self.login_admin_page.enter_email(email)
        self.login_admin_page.enter_password(password)
        self.login_manager_page.manager_authorization()
        self.login_manager_page.check_authorization(expected_result, expected_error_message)

import allure
import pytest

from pages.base_test import BaseTest


manager_email = "test-manager@test.ru"
manager_password = "12345678"
invalid_manager_email = "test-manager@test"
invalid_manager_password = "1234"


@allure.suite("Авторизация менеджера с разными данными")
@pytest.mark.parametrize(
        "email, password, expected_result, expected_error_message",
        [
            pytest.param(manager_email, manager_password, True, None,
                         id="Успешная авторизация"),
            pytest.param( invalid_manager_email, manager_password, False, "Значение «E-mail» не является правильным email адресом.",
                         id="Ошибка Email"),
            pytest.param(manager_email, invalid_manager_password, False, "Значение «Password» должно содержать минимум 8 символов.",
                         id="Ошибка password"),
        ],
)
class TestManagerLogin(BaseTest):


    @allure.title("Авторизация успешная")
    def test_login_manager(self, email, password, expected_result, expected_error_message):
        self.base_page.open_host()
        self.login_manager_page.open_manager_login_page()
        self.login_manager_page.enter_email(email)
        self.login_manager_page.enter_password(password)
        self.login_manager_page.manager_authorization()
        self.login_manager_page.check_authorization(expected_result, expected_error_message)
#1
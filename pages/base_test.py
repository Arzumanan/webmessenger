import pytest

from pages.base_page import BasePage
from pages.login_manager_page import LoginManagerPage


class BaseTest:
    base_page: BasePage
    login_manager_page: LoginManagerPage

    @pytest.fixture(autouse=True)
    def setup(self, request, browser):
        request.cls.browser = browser
        request.cls.base_page = BasePage(browser)
        request.cls.login_manager_page = LoginManagerPage(browser)
#1
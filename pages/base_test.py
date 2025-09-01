import pytest

from pages.base_page import BasePage
from pages.login_admin_page import LoginAdminPage
from pages.login_manager_page import LoginManagerPage
from pages.templates_page import TemplatesPage
from pages.managers_page import ManagersPage


class BaseTest:
    base_page: BasePage
    login_manager_page: LoginManagerPage
    login_admin_page: LoginAdminPage
    templates_page: TemplatesPage
    managers_page: ManagersPage

    @pytest.fixture(autouse=True)
    def setup(self, request, browser):
        request.cls.browser = browser
        request.cls.base_page = BasePage(browser)
        request.cls.login_manager_page = LoginManagerPage(browser)
        request.cls.login_admin_page = LoginAdminPage(browser)
        request.cls.templates_page = TemplatesPage(browser)
        request.cls.managers_page = ManagersPage(browser)

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.dialogs.base_dialogs import BaseDialogsPage
from pages.login_manager_page import LoginManagerPage
from config.data import manager_email, manager_password


@allure.suite("Проверка функциональности показа истекших диалогов")
class TestShowExpiredDialogs:

    @allure.title("Тест включения переключателя показа истекших диалогов")
    def test_show_expired_dialogs_toggle(self, browser):
        """
        Тест проверяет:
        1. Авторизацию под admin_ura (автоматически переходит в диалоги)
        2. Нажатие на кнопку фильтра
        3. Появление надписи "Показать просроченные диалоги"
        4. Включение переключателя показа истекших диалогов
        5. Проверку, что переключатель включился
        """
        # Создаем экземпляр страницы диалогов
        dialogs_page = BaseDialogsPage(browser)
        
        # Выполняем авторизацию admin_ura (автоматически переходит в диалоги)
        dialogs_page.login_as_manager()
        
        # Нажимаем на кнопку фильтра
        dialogs_page.click_filter_toggle_button()
        
        # Проверяем, что появилась надпись "Показать просроченные диалоги"
        text_appeared = dialogs_page.verify_expired_dialogs_text_appeared()
        assert text_appeared, "Надпись 'Показать просроченные диалоги' не появилась"
 
        # Включаем переключатель показа истекших диалогов
        dialogs_page.toggle_expired_dialogs_filter()
        
        # Проверяем, что переключатель включился
        is_toggle_enabled = dialogs_page.verify_expired_dialogs_toggle_enabled()
        
        assert is_toggle_enabled, "Переключатель показа истекших диалогов не включился"
        


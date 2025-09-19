import pytest
import allure
from pages.base_test import BaseTest

@allure.suite("Настройки диалога")
class TestDialogSettings(BaseTest):

    @allure.title("Активация настройки 'Оставлять сообщения непрочитанными'")
    def test_activate_leave_messages_unread(self, admin_authorized):
        self.dialog_settings_page.open()

        # Деактивируем элемент и проверяем результат
        self.dialog_settings_page.check_and_deactivate_leave_messages_unread()
        self.dialog_settings_page.check_deactivate_leave_messages_unread()

        # Активируем элемент и проверяем результат
        self.dialog_settings_page.check_and_activate_leave_messages_unread()
        self.dialog_settings_page.check_activate_leave_messages_unread()

    @allure.title("Деактивация настройки 'Оставлять сообщения непрочитанными'")
    def test_deactivate_leave_messages_unread(self, admin_authorized):
        self.dialog_settings_page.open()

        # Активируем элемент и проверяем результат
        self.dialog_settings_page.check_and_activate_leave_messages_unread()
        self.dialog_settings_page.check_activate_leave_messages_unread()

        # Деактивируем элемент и проверяем результат
        self.dialog_settings_page.check_and_deactivate_leave_messages_unread()
        self.dialog_settings_page.check_deactivate_leave_messages_unread()

    @allure.title("Активация настройки 'Присвоение даты контакта'")
    def test_activate_assign_contact_date(self, admin_authorized):
        self.dialog_settings_page.open()

        # Деактивируем элемент и проверяем результат
        self.dialog_settings_page.check_and_deactivate_assign_contact_date()
        self.dialog_settings_page.check_deactivate_assign_contact_date()

        # Активируем элемент и проверяем результат
        self.dialog_settings_page.check_and_activate_assign_contact_date()
        self.dialog_settings_page.check_activate_assign_contact_date()

    @allure.title("Деактивация настройки 'Присвоение даты контакта'")
    def test_deactivate_assign_contact_date(self, admin_authorized):
        self.dialog_settings_page.open()

        # Активируем элемент и проверяем результат
        self.dialog_settings_page.check_and_activate_assign_contact_date()
        self.dialog_settings_page.check_activate_assign_contact_date()

        # Деактивируем элемент и проверяем результат
        self.dialog_settings_page.check_and_deactivate_assign_contact_date()
        self.dialog_settings_page.check_deactivate_assign_contact_date()
"""Тесты для страницы разрешений менеджера."""
import pytest
import allure
from pages.base_test import BaseTest

@allure.suite("Разрешения менеджера")
class TestPermissionsManager(BaseTest):

    @allure.title("Активация тестового тега 1")
    def test_activate_tag(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_deactivate_test_tag_1()
        self.permissions_manager_page.click_toggle_test_tag_1()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_activate_test_tag_1()
    
    @allure.title("Деактивация тестового тега 1")
    def test_deactivate_tag(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_activate_test_tag_1()
        self.permissions_manager_page.click_toggle_test_tag_1()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_deactivate_test_tag_1()

    @allure.title("Активация тестового статуса 1")
    def test_activate_status(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_deactivate_test_status_1()
        self.permissions_manager_page.click_toggle_test_status_1()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_activate_test_status_1()

    @allure.title("Деактивация тестового статуса 1")
    def test_deactivate_status(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_activate_test_status_1()
        self.permissions_manager_page.click_toggle_test_status_1()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_deactivate_test_status_1()
    
    @allure.title("Активация разрешения 'Сохранить доступ к диалогам'")
    def test_activate_save_dialog_access(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_deactivate_save_dialog_access()
        self.permissions_manager_page.click_toggle_save_dialog_access()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_activate_save_dialog_access()

    @allure.title("Деактивация разрешения 'Сохранить доступ к диалогам'")
    def test_deactivate_save_dialog_access(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_activate_save_dialog_access()
        self.permissions_manager_page.click_toggle_save_dialog_access()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_deactivate_save_dialog_access()

    @allure.title("Активация разрешения 'Редактировать информацию о диалогах'")
    def test_activate_edit_dialog_info(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_deactivate_edit_dialog_info()   
        self.permissions_manager_page.click_toggle_edit_dialog_info()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_activate_edit_dialog_info()

    @allure.title("Деактивация разрешения 'Редактировать информацию о диалогах'")
    def test_deactivate_edit_dialog_info(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_activate_edit_dialog_info()
        self.permissions_manager_page.click_toggle_edit_dialog_info()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_deactivate_edit_dialog_info()

    @allure.title("Активация разрешения 'Просмотр контактной информации'")
    def test_activate_view_contact_info(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_deactivate_view_contact_info()
        self.permissions_manager_page.click_toggle_view_contact_info()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_activate_view_contact_info()    

    @allure.title("Деактивация разрешения 'Просмотр контактной информации'")
    def test_deactivate_view_contact_info(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_activate_view_contact_info()
        self.permissions_manager_page.click_toggle_view_contact_info()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_deactivate_view_contact_info()

    @allure.title("Активация разрешения 'Выгружать контакты'")
    def test_activate_export_contacts(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_deactivate_export_contacts()
        self.permissions_manager_page.click_toggle_export_contacts()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_activate_export_contacts()

    @allure.title("Деактивация разрешения 'Выгружать контакты'")
    def test_deactivate_export_contacts(self, admin_authorized):
        self.permissions_manager_page.open()
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_and_activate_export_contacts()
        self.permissions_manager_page.click_toggle_export_contacts()
        self.permissions_manager_page.click_save_button()   
        self.permissions_manager_page.go_to_manager_permissions()
        self.permissions_manager_page.check_deactivate_export_contacts()
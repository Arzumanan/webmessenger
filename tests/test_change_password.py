"""
Тесты для страницы смены пароля
"""
import pytest
import allure
from pages.profile.change_password_page import ChangePasswordPage
from pages.base_test import BaseTest
from config.data import admin_email, admin_password


class TestChangePassword(BaseTest):
    """Класс тестов для смены пароля"""
    
    @allure.title("Успешная смена пароля")
    def test_successful_password_change(self):
        """Тест успешной смены пароля"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        # Данные для смены пароля
        current_password = admin_password
        new_password = "NewPassword123!"
        
        with allure.step("Смена пароля"):
            # Выполнение смены пароля
            self.change_password_page.change_password(
                current_password=current_password,
                new_password=new_password
            )
            
            # Проверка успешного сообщения
            assert self.change_password_page.is_success_message_displayed(), \
                "Сообщение об успешной смене пароля не отображается"
            
            success_message = self.change_password_page.get_success_message_text()
            assert "успешно" in success_message.lower() or "изменен" in success_message.lower(), \
                f"Неожиданное сообщение об успехе: {success_message}"
    
    @allure.title("Смена пароля с неверным текущим паролем")
    def test_password_change_with_wrong_current_password(self):
        """Тест смены пароля с неверным текущим паролем"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        # Данные с неверным текущим паролем
        wrong_current_password = "WrongPassword123!"
        new_password = "NewPassword123!"
        
        with allure.step("Попытка смены пароля с неверным текущим паролем"):
            # Выполнение смены пароля
            self.change_password_page.change_password(
                current_password=wrong_current_password,
                new_password=new_password
            )
            
            # Проверка сообщения об ошибке
            assert self.change_password_page.is_error_message_displayed(), \
                "Сообщение об ошибке не отображается"
            
            error_message = self.change_password_page.get_error_message_text()
            assert "неверный" in error_message.lower() or "неправильный" in error_message.lower() or "ошибка" in error_message.lower(), \
                f"Неожиданное сообщение об ошибке: {error_message}"
    
    @allure.title("Смена пароля с несовпадающими новыми паролями")
    def test_password_change_with_mismatched_passwords(self):
        """Тест смены пароля с несовпадающими новыми паролями"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        # Данные с несовпадающими паролями
        current_password = admin_password
        new_password = "NewPassword123!"
        confirm_password = "DifferentPassword456!"
        
        with allure.step("Попытка смены пароля с несовпадающими новыми паролями"):
            # Выполнение смены пароля
            self.change_password_page.change_password(
                current_password=current_password,
                new_password=new_password,
                confirm_password=confirm_password
            )
            
            # Проверка сообщения об ошибке
            assert self.change_password_page.is_error_message_displayed(), \
                "Сообщение об ошибке не отображается"
            
            error_message = self.change_password_page.get_error_message_text()
            assert "не совпадают" in error_message.lower() or "не совпадают" in error_message.lower() or "разные" in error_message.lower(), \
                f"Неожиданное сообщение об ошибке: {error_message}"
    
    @allure.title("Смена пароля с пустыми полями")
    def test_password_change_with_empty_fields(self):
        """Тест смены пароля с пустыми полями"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        with allure.step("Попытка смены пароля с пустыми полями"):
            # Очистка всех полей
            self.change_password_page.clear_all_fields()
            
            # Проверка, что кнопка сохранения неактивна
            assert not self.change_password_page.is_save_button_enabled(), \
                "Кнопка сохранения должна быть неактивна при пустых полях"
    
    @allure.title("Отмена смены пароля")
    def test_cancel_password_change(self):
        """Тест отмены смены пароля"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        # Заполнение полей
        current_password = admin_password
        new_password = "NewPassword123!"
        
        with allure.step("Заполнение полей и отмена смены пароля"):
            self.change_password_page.enter_current_password(current_password)
            self.change_password_page.enter_new_password(new_password)
            self.change_password_page.enter_confirm_password(new_password)
            
            # Нажатие кнопки отмены
            self.change_password_page.click_cancel_button()
            
            # Проверка, что поля очищены или страница закрыта
            # (зависит от реализации интерфейса)
            # Здесь можно добавить дополнительные проверки

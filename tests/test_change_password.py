"""
Тесты для страницы смены пароля
"""
from time import sleep
import pytest
import allure
from pages.profile.change_password_page import ChangePasswordPage
from pages.base_test import BaseTest
from config.data import admin2_email, admin2_password


class TestChangePassword(BaseTest):
    """Класс тестов для смены пароля"""
    
    @allure.title("Успешная смена пароля")
    def test_successful_password_change(self):
        """Тест успешной смены пароля"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        # Данные для смены пароля
        current_password = admin2_password
        new_password = "12345678"
        

        # with allure.step("Сохранение пустой формы"):
        #    self.change_password_page.save_empty_password(current_password)
            
        #     # Проверка сообщения об ошибке
        # assert self.change_password_page.is_error_message_displayed(), \
        #         "Сообщение об ошибке не отображается"
            

        # error_message = self.change_password_page.get_error_message_text()
        # assert "не может быть пустым" in error_message.lower() or "не может быть пустым" in error_message.lower() or "обязательное поле" in error_message.lower(), \
        #         f"Неожиданное сообщение об ошибке: {error_message}"

        with allure.step("Смена пароля"):
            # Выполнение смены пароля
            self.change_password_page.change_password(
                current_password=current_password,
                new_password=new_password
               
            )
            sleep(2)
            # Проверка URL после смены пароля
            expected_url = "https://testim.i2crm.ru/login"
            current_url = self.browser.current_url
            
            assert expected_url in current_url, \
                f"Ожидался URL содержащий '{expected_url}', а получили '{current_url}'"
            
            print(f"✅ Успешная проверка URL: {current_url}")
            
            # Проверка успешного сообщения
            # assert self.change_password_page.is_success_message_displayed(), \
            #    "Сообщение об успешной смене пароля не отображается"
            
            # success_message = self.change_password_page.get_success_message_text()
            # assert "успешно" in success_message.lower() or "изменен" in success_message.lower(), \
            #    f"Неожиданное сообщение об успехе: {success_message}"
    
    @allure.title("Смена пароля с неверным текущим паролем")
    def test_password_change_with_wrong_current_password(self):
        """Тест смены пароля с неверным текущим паролем"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
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
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        # Данные с несовпадающими паролями
        current_password = admin2_password
        new_password = "NewPassword123!"
        confirm_password = "DifferentPassword456!"
        
        with allure.step("Попытка смены пароля с несовпадающими новыми паролями"):
            # Выполнение смены пароля
            self.change_password_page.change_password(
                current_password=current_password,
                new_password=new_password,
                confirm_password=confirm_password
            )
            sleep(2)
            # Проверка сообщения об ошибке
            # assert self.change_password_page.is_error_message_displayed(), \
            #     "Сообщение об ошибке не отображается"
            
            error_message = self.change_password_page.get_error_message_text2()
            assert "должны совпадать" in error_message.lower() or "должны совпадать" in error_message.lower() or "разные" in error_message.lower(), \
                f"Неожиданное сообщение об ошибке: {error_message}"
    
    @allure.title("Смена пароля с пустыми полями")
    def test_password_change_with_empty_fields(self):
        """Тест смены пароля с пустыми полями"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
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
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        # Заполнение полей
        current_password = admin2_password
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
    
    @allure.title("Проверка валидации пустых полей")
    def test_empty_fields_validation(self):
        """Тест проверки, что форма не отправляется с пустыми полями"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        with allure.step("Попытка сохранения формы с пустыми полями"):
            # Очистка всех полей (если они были заполнены)
            self.change_password_page.clear_all_fields()
            
            # Попытка сохранить форму с пустыми полями
            self.change_password_page.click_save_button()
            
            # Проверка, что отображается сообщение об ошибке
            assert self.change_password_page.get_error_message_text2(), \
                "Сообщение об ошибке должно отображаться при пустых полях"
            
            error_message = self.change_password_page.get_error_message_text2()
            assert error_message, "Сообщение об ошибке не должно быть пустым"
            
            # Проверка содержания сообщения об ошибке
            expected_errors = [
                "не может быть пустым",
                "обязателен для заполнения", 
                "заполните поле",
                "введите старый пароль",
                "required",
                "empty"
            ]
            
            error_found = any(error in error_message.lower() for error in expected_errors)
            assert error_found, \
                f"Сообщение об ошибке должно содержать информацию о пустых полях. Получено: {error_message}"
            
            print(f"✅ Валидация пустых полей работает корректно. Сообщение: {error_message}")
    
    @allure.title("Проверка валидации частично заполненных полей")
    def test_partially_filled_fields_validation(self):
        """Тест проверки валидации при частично заполненных полях"""
        # Логин как админ
        self.change_password_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу смены пароля
        self.change_password_page.open_change_password_page()
        
        test_cases = [
            {
                "name": "Только текущий пароль",
                "current": admin2_password,
                "new": "",
                "confirm": ""
            },
            {
                "name": "Только новый пароль",
                "current": "",
                "new": "NewPassword123!",
                "confirm": ""
            },
            {
                "name": "Текущий и новый пароль без подтверждения",
                "current": admin2_password,
                "new": "NewPassword123!",
                "confirm": ""
            }
        ]
        
        for test_case in test_cases:
            with allure.step(f"Тест: {test_case['name']}"):
                # Очистка полей
                self.change_password_page.clear_all_fields()
                
                # Заполнение полей согласно тест-кейсу
                if test_case['current']:
                    self.change_password_page.enter_current_password(test_case['current'])
                if test_case['new']:
                    self.change_password_page.enter_new_password(test_case['new'])
                if test_case['confirm']:
                    self.change_password_page.enter_confirm_password(test_case['confirm'])
                
                # Попытка сохранить
                self.change_password_page.click_save_button()
                
                # Проверка, что отображается ошибка
                assert self.change_password_page.get_error_message_text2(), \
                    f"Ошибка должна отображаться для случая: {test_case['name']}"
                
                error_message = self.change_password_page.get_error_message_text2()
                assert error_message, f"Сообщение об ошибке не должно быть пустым для случая: {test_case['name']}"
                
                print(f"✅ {test_case['name']}: {error_message}")

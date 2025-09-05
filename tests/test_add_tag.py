import allure
import pytest
from config.data import admin_email, admin_password
from pages.base_test import BaseTest


@allure.feature("Управление тегами")
@allure.story("Создание и редактирование тегов")
class TestTagManagement(BaseTest):
    
    @allure.title("Тест создания и удаления тега")
    @allure.description("""
    Тест выполняет следующие действия:
    1. Авторизация администратором
    2. Переход на страницу тегов
    3. Создание нового тега
    """)
    def test_create_and_delete_tag(self):
        # Генерируем случайный тег
        test_tag = self.tags_page.generate_random_tag(4, 17)
        
        with allure.step("1. Авторизация администратором"):
            self.login_admin_page.login_as_admin(admin_email, admin_password)
            
        with allure.step("2. Переход на страницу тегов"):
            self.tags_page.open_tags_page()
            
        with allure.step("3. Создание нового тега"):
            self.tags_page.create_tag(test_tag)
            
            # Проверяем, что тег был создан
            assert self.tags_page.is_tag_present(test_tag), f"Тег '{test_tag}' не был создан"
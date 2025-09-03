import random
import string

import allure

from config.data import admin_email, admin_password
from pages.base_test import BaseTest


def _rand(n=6):
    return ''.join(random.choices(string.ascii_letters, k=n))


@allure.suite("Группы шаблонов")
class TestTemplateGroup(BaseTest):

    @allure.title("Полный цикл группы шаблонов")
    def test_template_group_full_cycle(self):
        # Генерируем названия группы (максимум 30 символов)
        original_name = f"TestGroup-{_rand(6)}"[:30]
        updated_name = f"Updated-{_rand(6)}"[:30]
        
        print(f"\n🔄 ПОЛНЫЙ ЦИКЛ ГРУППЫ ШАБЛОНОВ")
        print(f"📝 Исходное: {original_name}")
        print(f"📝 Новое: {updated_name}")
        
        # Авторизация и переход в раздел
        self.base_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()
        
        self.templates_page.open_settings_and_check()
        self.templates_page.open_templates()

        # Создание группы
        with allure.step("Создание группы"):
            self.templates_page.open_add_group_modal()
            self.templates_page.fill_group_name(original_name)
            self.templates_page.create_template_group()
            self.templates_page.assert_group_in_list(original_name)
            print(f"✅ Создана: {original_name}")

        # Редактирование группы
        with allure.step("Редактирование группы"):
            self.templates_page.open_edit_group_modal(original_name)
            self.templates_page.update_group_name(updated_name)
            self.templates_page.save_group_changes()
            self.templates_page.assert_group_in_list(updated_name)
            print(f"✅ Переименована: {updated_name}")

        # Удаление группы
        with allure.step("Удаление группы"):
            self.templates_page.delete_group_by_name(updated_name)
            self.templates_page.assert_group_not_in_list(updated_name)
            print(f"✅ Удалена: {updated_name}")
        
        print(f"\n🎉 ПОЛНЫЙ ЦИКЛ ЗАВЕРШЕН")

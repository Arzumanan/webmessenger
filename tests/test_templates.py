import random
import string

import allure
import pytest

from config.data import admin_email, admin_password
from pages.base_test import BaseTest


def _rand(n=6):
    return ''.join(random.choices(string.ascii_letters, k=n))


@allure.suite("Шаблоны: создание")
class TestTemplates(BaseTest):

    @allure.title("Валидация: пустое имя шаблона")
    def test_validation_empty_name(self):
        self.base_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()

        self.templates_page.open_settings_and_check()
        self.templates_page.open_templates()
        self.templates_page.open_add_modal()
        # Пустое имя, валидный текст
        self.templates_page.fill_template_form(name="", category=None, text=f"txt-{_rand(6)}")
        self.templates_page.save_template()
        from selenium.webdriver.common.by import By
        self.templates_page.element_in_visible((By.XPATH, "//*[contains(@class,'error') and contains(.,'Название') or contains(.,'Обязательное поле') or contains(.,'Введите')]"))

    @allure.title("Создание и удаление шаблона: полный цикл")
    def test_create_and_delete_template_cycle(self):
        # Логин как админ
        self.base_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin_email)
        self.login_admin_page.enter_password(admin_password)
        self.login_admin_page.admin_authorization()

        # Переход в Настройки и проверка заголовка
        self.templates_page.open_settings_and_check()

        # Открыть страницу шаблонов (прямая ссылка)
        self.templates_page.open_templates()

        # Данные шаблона
        name = f"CycleTpl-{_rand(5)}"
        text = f"Шаблон для полного цикла {_rand(10)}"

        # ===== КЕЙС 1: СОЗДАНИЕ ШАБЛОНА =====
        print(f"\n🔄 КЕЙС 1: СОЗДАНИЕ ШАБЛОНА")
        print(f"📝 Имя шаблона: {name}")
        print(f"📄 Текст шаблона: {text}")
        
        with allure.step("КЕЙС 1: Создание шаблона"):
            # Создать шаблон
            self.templates_page.open_add_modal()
            self.templates_page.fill_template_form(name=name, category=None, text=text)
            self.templates_page.save_template()

            # Проверка наличия в списке
            self.templates_page.assert_template_in_list(name)
            print(f"✅ РЕЗУЛЬТАТ КЕЙСА 1: Шаблон '{name}' успешно создан и найден в списке")
        
        # ===== КЕЙС 2: УДАЛЕНИЕ ШАБЛОНА =====
        print(f"\n🗑️ КЕЙС 2: УДАЛЕНИЕ ШАБЛОНА")
        print(f"🎯 Цель: Удалить шаблон '{name}'")
        
        with allure.step("КЕЙС 2: Удаление шаблона"):
            # Удаление созданного шаблона
            self.templates_page.delete_template_by_name(name)
            
            # Проверка отсутствия в списке после удаления
            self.templates_page.assert_template_not_in_list(name)
            print(f"✅ РЕЗУЛЬТАТ КЕЙСА 2: Шаблон '{name}' успешно удален и отсутствует в списке")
        
        # ===== ИТОГОВЫЙ РЕЗУЛЬТАТ =====
        print(f"\n🎉 ИТОГОВЫЙ РЕЗУЛЬТАТ:")
        print(f"   ✅ Создание шаблона: УСПЕШНО")
        print(f"   ✅ Удаление шаблона: УСПЕШНО")
        print(f"   📊 Полный цикл: ЗАВЕРШЕН")


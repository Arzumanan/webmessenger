import random
import string
import pytest
from config.data import admin_email, admin_password
from pages.base_test import BaseTest


def random_string(length=8):
    """Генерация случайной строки"""
    return ''.join(random.choices(string.ascii_letters, k=length))


def random_email():
    """Генерация случайного email"""
    return random_string(6) + "@test.com"


class TestCreateManager(BaseTest):
    """Тест создания и удаления менеджера"""

    def test_create_and_delete_manager(self):
        """Тест полного цикла: создание и удаление менеджера"""
        # Генерируем случайные данные для менеджера
        name = random_string(6)
        email = random_email()
        password = random_string(10)

        # Авторизуемся как администратор
        self.login_admin_page.login_as_admin(admin_email, admin_password)
        print("✅ Авторизация администратора успешна")

        # Создаем нового менеджера
        created_email = self.managers_page.create_new_manager(name, email, password)
        print(f"✅ Менеджер создан и отображается в списке: {created_email}")

        # Удаляем созданного менеджера
        self.managers_page.delete_manager(created_email)
        print(f"✅ Менеджер удалён: {created_email}")

        # Закрываем баннер уведомлений если появился
        self.base_page.dismiss_notifications_banner()


if __name__ == "__main__":
    pytest.main([__file__])
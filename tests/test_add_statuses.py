import allure
import pytest
from pages.base_test import BaseTest
from time import sleep


@allure.suite("Создание и управление статусами")
class TestStatusManagement(BaseTest):

    @allure.title("Создание и удаление статуса")
    @allure.description("Базовый тест создания и удаления статуса с автогенерацией названия")
    def test_create_and_delete_status_success(self, admin_authorized):
        self.status_page.open_status_page()
        # Создаем статус с автогенерацией
        created_status = self.status_page.create_status()
        # Проверяем создание
        self.status_page.is_status_present(created_status)
        # Удаляем статус
        self.status_page.delete_status(created_status)
        # Проверяем удаление
        self.status_page.is_status_not_present(created_status)

    @allure.title("Редактирование статуса")
    def test_edit_status_success(self, admin_authorized):
        self.status_page.open_status_page()
        # Создаем статус для редактирования
        original_status = self.status_page.create_status()
        # Проверяем, что статус создан
        self.status_page.is_status_present(original_status)
        # Редактируем статус с выбором цвета
        new_status = self.status_page.generate_random_status()
        self.status_page.edit_status(original_status, new_status, color_index=3)
        # Проверяем, что старый статус исчез
        self.status_page.is_status_not_present(original_status)
        # Проверяем, что новый статус появился
        self.status_page.is_status_present(new_status)
        # Очищаем - удаляем отредактированный статус
        self.status_page.delete_status(new_status)
        self.status_page.is_status_not_present(new_status)

    @allure.title("Создание статуса с коротким названием")
    def test_create_short_status_error(self, admin_authorized):
        self.status_page.open_status_page()
        self.status_page.click_add_status_button()
        short_random_status = self.status_page.generate_random_status(1, 3)
        self.status_page.input_status_field(short_random_status)
        self.status_page.click_submit_add_status_button()
        self.status_page.check_error_short_status()

    @allure.title("Создание статуса с ошибкой выбора цвета")
    def test_create_status_with_error_color(self, admin_authorized):
        self.status_page.open_status_page()
        self.status_page.click_add_status_button()
        self.status_page.element_in_visible(self.status_page.MODAL_HEADER)
        self.status_page.input_status_field(self.status_page.generate_random_status())
        self.status_page.click_submit_add_status_button()
        self.status_page.check_error_color_status()
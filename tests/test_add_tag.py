import allure
import pytest
from pages.base_test import BaseTest


@allure.suite("Создание и управление тегами")
class TestTagManagement(BaseTest):
    @allure.title("Создание и удаление тега")
    @allure.description("Базовый тест создания и удаления тега с автогенерацией названия")
    def test_create_and_delete_tag_success(self, admin_authorized):
        self.tags_page.open_tags_page()
        # Создаем тег с автогенерацией
        created_tag = self.tags_page.create_tag()
        # Проверяем создание
        self.tags_page.is_tag_present(created_tag)
        # Удаляем тег
        self.tags_page.delete_tag(created_tag)
        # Проверяем удаление
        self.tags_page.is_tag_not_present(created_tag)

    @allure.title("Редактирование тега")
    def test_edit_tag_success(self, admin_authorized):
        self.tags_page.open_tags_page()
        # Создаем тег для редактирования
        original_tag = self.tags_page.create_tag()
        # Проверяем, что тег создан
        self.tags_page.is_tag_present(original_tag)
        # Редактируем тег
        new_tag = self.tags_page.generate_random_tag()
        self.tags_page.edit_tag(original_tag, new_tag)
        # Проверяем, что старый тег исчез
        self.tags_page.is_tag_not_present(original_tag)
        # Проверяем, что новый тег появился
        self.tags_page.is_tag_present(new_tag)
        # Очищаем - удаляем отредактированный тег
        self.tags_page.delete_tag(new_tag)
        self.tags_page.is_tag_not_present(new_tag)

    @allure.title("Создание тега с коротким названием")
    def test_create_short_tag_error(self, admin_authorized):
        self.tags_page.open_tags_page()
        self.tags_page.click_add_tag_button()
        short_random_tag = self.tags_page.generate_random_tag(1, 3)
        self.tags_page.input_tag_field(short_random_tag)
        self.tags_page.click_submit_add_tag_button()
        self.tags_page.check_error_short_tag()

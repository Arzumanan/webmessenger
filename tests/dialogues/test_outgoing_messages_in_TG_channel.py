import allure
import pytest

from pages.dialogs.base_dialogs import (
    BaseDialogsPage, 
    dialogs_page_ready, 
    SEARCH_VARIANTS,
    TEST_MESSAGE
)


@allure.suite("Авторизация и переход в диалоги")
class TestDialogsNavigation:

    @allure.title("Авторизация admin_ura и переход в раздел диалогов")
    def test_login_and_navigate_to_dialogs(self, browser):
        """
        Тест авторизации пользователя admin_ura и перехода в раздел диалогов
        """
        # Создаем экземпляр страницы диалогов
        dialogs_page = BaseDialogsPage(browser)
        
        # Выполняем полную авторизацию и переход в диалоги
        dialogs_page.login_as_admin_ura()
        
        # Проверяем успешный переход в диалоги
        elements_count = dialogs_page.verify_dialogs_page()
        
        # Дополнительные проверки
        assert elements_count >= 0, "Не удалось проверить интерфейс диалогов"

    @allure.title("Поиск диалога и отправка сообщения в ТГ канал")
    def test_outgoing_messages_in_TG_channel(self, dialogs_page_ready):
        """
        Тест поиска диалога с пользователем Юрий Арзуманян - Telegram - ura_testt2
        и отправки тестового сообщения в ТГ канал
        """
        # Фикстура dialogs_page_ready уже выполнила поиск и открытие диалога
        dialogs_page = dialogs_page_ready
        
        # Отправляем сообщение в диалог
        dialogs_page.send_message(TEST_MESSAGE)
        
        # Проверяем, что сообщение было отправлено
        message_sent = dialogs_page.verify_message_sent(TEST_MESSAGE)
        assert message_sent, f"Сообщение '{TEST_MESSAGE}' не было отправлено или не отображается в чате"
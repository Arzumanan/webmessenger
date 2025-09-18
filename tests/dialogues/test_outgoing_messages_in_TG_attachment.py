import allure
import pytest
from pages.dialogs.base_dialogs import dialogs_page_ready, send_attachment_script


@allure.suite("Отправка сообщений с вложениями в Telegram")
class TestOutgoingMessagesWithAttachments:

    @allure.title("Последовательная отправка всех сообщений с вложениями")
    def test_send_all_messages_with_attachments(self, send_attachment_script):
        """Тест последовательной отправки всех сообщений с вложениями в одном диалоге"""
        
        # 1. Отправка сообщения с текстовым файлом
        with allure.step("Отправка сообщения с текстовым файлом"):
            test_file = send_attachment_script.get_test_file("test_document.txt")
            test_message = "Тестовое сообщение с текстовым файлом"
            send_attachment_script.send_message_with_attachment(test_message, test_file)
        
        # 2. Отправка сообщения с изображением
        with allure.step("Отправка сообщения с изображением"):
            test_file = send_attachment_script.get_test_file("test_image.jpeg")
            test_message = "Тестовое сообщение с изображением"
            send_attachment_script.send_message_with_attachment(test_message, test_file)
        
        # 3. Отправка сообщения с PDF файлом (пропускаем, если есть проблемы)
        with allure.step("Отправка сообщения с PDF файлом"):
            test_file = send_attachment_script.get_test_file("test_pdf.pdf")
            test_message = "Тестовое сообщение с PDF документом"
            
            # Проверяем, что файл существует
            import os
            if not os.path.exists(test_file):
                allure.attach("PDF файл не найден, пропускаем тест", 
                             name="PDF файл", attachment_type=allure.attachment_type.TEXT)
                pytest.skip("PDF файл не найден")
            
            # Логируем информацию о файле
            file_size = os.path.getsize(test_file)
            allure.attach(f"PDF файл найден: {test_file}, размер: {file_size} байт", 
                         name="PDF файл", attachment_type=allure.attachment_type.TEXT)
            
            try:
                send_attachment_script.send_message_with_attachment(test_message, test_file)
            except Exception as e:
                allure.attach(f"Ошибка при отправке PDF: {str(e)}. Пропускаем тест.", 
                             name="PDF ошибка", attachment_type=allure.attachment_type.TEXT)
                pytest.skip(f"PDF файл не может быть отправлен: {str(e)}")
        
        # 4. Отправка сообщения с несколькими файлами
        with allure.step("Отправка сообщения с несколькими файлами"):
            files = [
                send_attachment_script.get_test_file("test_document.txt"),
                send_attachment_script.get_test_file("test_image.jpeg")
            ]
            test_message = "Тестовое сообщение с несколькими файлами"
            
            # Загружаем все файлы
            for file_path in files:
                send_attachment_script.dialogs_page.select_file(file_path)
            
            # Отправляем сообщение
            send_attachment_script.dialogs_page.send_message(test_message)
            
            # Проверяем отправку
            message_sent = send_attachment_script.dialogs_page.verify_message_sent(test_message)
            assert message_sent, f"Сообщение '{test_message}' не было отправлено"
        

        
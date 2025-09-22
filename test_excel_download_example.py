"""
Пример теста для скачивания и открытия Excel файла с локатором EXPORT_EXCEL_BUTTON
"""
import os
import sys
import time
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.contacts.contacts_page import ContactsPage
from pages.login_admin_page import LoginAdminPage
from config.data import admin2_email, admin2_password


class ExcelDownloadTest:
    """Класс для тестирования скачивания Excel файла"""
    
    def __init__(self):
        self.browser = None
        self.contacts_page = None
        self.login_page = None
    
    def setup_browser(self):
        """Настройка браузера для скачивания файлов"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Настройки для скачивания файлов
        prefs = {
            "download.default_directory": os.path.join(os.getcwd(), "downloads"),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        self.browser = webdriver.Chrome(options=chrome_options)
        self.contacts_page = ContactsPage(self.browser)
        self.login_page = LoginAdminPage(self.browser)
    
    @allure.step("Авторизация в системе")
    def login(self):
        """Вход в систему как администратор"""
        self.contacts_page.open_host()
        self.login_page.open_admin_login_page()
        self.login_page.enter_email(admin2_email)
        self.login_page.enter_password(admin2_password)
        self.login_page.admin_authorization()
    
    @allure.step("Переход на страницу контактов")
    def open_contacts(self):
        """Открытие страницы контактов"""
        self.contacts_page.open_contacts_page()
    
    @allure.step("Скачивание Excel файла")
    def download_excel(self):
        """Скачивание Excel файла с контактами"""
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)
        
        # Скачиваем файл
        file_path = self.contacts_page.download_excel_file(download_dir)
        
        # Проверяем, что файл скачался
        assert os.path.exists(file_path), f"Файл не найден: {file_path}"
        assert os.path.getsize(file_path) > 0, "Файл пустой"
        
        print(f"✅ Excel файл скачан: {file_path}")
        return file_path
    
    @allure.step("Проверка содержимого файла")
    def verify_file_content(self, file_path):
        """Проверка содержимого Excel файла"""
        try:
            # Читаем Excel файл
            df = pd.read_excel(file_path)
            
            # Проверяем, что файл не пустой
            assert not df.empty, "Excel файл пустой"
            
            print(f"✅ Файл содержит {len(df)} строк и {len(df.columns)} колонок")
            print(f"📊 Колонки: {list(df.columns)}")
            
            # Выводим первые несколько строк
            print("\n📋 Первые 5 строк данных:")
            print(df.head().to_string())
            
            return df
            
        except Exception as e:
            print(f"❌ Ошибка при чтении файла: {e}")
            raise
    
    @allure.step("Открытие файла в системе")
    def open_file(self, file_path):
        """Открытие Excel файла в системе"""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
            
            print(f"✅ Файл открыт: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при открытии файла: {e}")
            return False
    
    def run_test(self):
        """Запуск полного теста"""
        try:
            print("🚀 Запуск теста скачивания Excel файла...")
            
            # Настройка браузера
            self.setup_browser()
            
            # Авторизация
            self.login()
            
            # Переход на страницу контактов
            self.open_contacts()
            
            # Скачивание файла
            file_path = self.download_excel()
            
            # Проверка содержимого
            df = self.verify_file_content(file_path)
            
            # Открытие файла
            self.open_file(file_path)
            
            print("✅ Тест выполнен успешно!")
            print(f"📁 Файл сохранен: {file_path}")
            
            return file_path, df
            
        except Exception as e:
            print(f"❌ Ошибка в тесте: {e}")
            raise
        finally:
            # Закрываем браузер
            if self.browser:
                self.browser.quit()


def main():
    """Главная функция для запуска теста"""
    test = ExcelDownloadTest()
    try:
        file_path, df = test.run_test()
        print(f"\n🎉 Тест завершен успешно!")
        print(f"📊 Обработано {len(df)} контактов")
        print(f"📁 Файл: {file_path}")
    except Exception as e:
        print(f"\n💥 Тест завершился с ошибкой: {e}")


if __name__ == "__main__":
    main()

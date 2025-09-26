"""
Страница управления контактами
"""
from time import sleep
import allure
from pages.base_page import BasePage
import urllib.request
import os
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ContactsPage(BasePage):
    """Класс для работы со страницей контактов"""
    
    # Локаторы элементов страницы
    # Навигация
    CONTACTS_MENU =("xpath", "//a[@id='contacts']")
    RAZV_BUTTON = ("xpath", "//button[contains(@class, 'navbar-toggle')]")
    ADD_CONTACT_BUTTON = ("xpath", "//button[contains(text(), 'Добавить контакт')]")
    
    # Форма создания контакта
    CHANNEL_SELECT_OPEN = ("xpath", "//span[contains(text(), 'Выберите канал')]")
    CHANNEL_SELECT = ("xpath", "//li[contains(text(), 'whatsapp')]")
    CHANNEL_OPTION_ALL = ("xpath", "//span[contains(text(), 'Все каналы')]")
    CHANNEL_OPTION_INSTAGRAM = ("xpath", "//span[contains(text(), 'instagram')]")
    CHANNEL_OPTION_TELEGRAM =  ("xpath", "//span[contains(text(), 'telegram')]")
    CHANNEL_OPTION_WHATSAPP = ("xpath", "//option[@value='whatsapp']")
    CHANNEL_OPTION_VIBER = ("xpath", "//option[@value='viber']")
    CHANNEL_OPTION_SMS = ("xpath", "//option[@value='sms']")
    
    NAME_FIELD = ("xpath", "//input[@name='contactName']")
    LOGIN_FIELD = ("xpath", "//input[@name='defaultUsername']")
    PHONE_FIELD = ("xpath", "//input[@name='contactTelephone']")
    MESSAGE_FIELD = ("xpath", "//textarea[@name='contactMessage']")
    
    SAVE_CONTACT_BUTTON = ("xpath", "//button[@type='submit' and contains(text(), 'Добавить')]")
    CANCEL_BUTTON = ("xpath", "//button[contains(text(), 'Отменить')]")
    
    # Поиск и фильтрация
    SEARCH_FIELD = ("xpath", "//input[@class='sidebar-header-search-field-input']")
    SEARCH_BUTTON = ("xpath", "//button[contains(@class, 'search-btn')]")
    CHANNEL_FILTER_OPEN = ("xpath", "//span[contains(text(), 'Выберите канал')]")
    CHANNEL_FILTER = ("xpath", "//span[contains(text(), 'Каналы контактов')]")
    CHANNEL_FILTER_SELECT = ("xpath", "//span[@class='channel-select-option__label']")
    FILTER_BUTTON = ("xpath", "//button[contains(text(), 'Фильтровать')]")
    CLEAR_FILTER_BUTTON = ("xpath", "//button[contains(text(), 'Очистить фильтры')]")
    
    # Список контактов
    CONTACTS_LIST = ("xpath", "//div[@class='contacts-list']")
    CONTACT_ITEM = ("xpath", "//div[@class='contact-card']")
    CONTACT_NAME = ("xpath", "//div[@class='contact-card']")
    CONTACT_NAME_INSTAGRAM = ("xpath", "//p[@class='contact-card__username']")
    CONTACT_CHANNEL = ("xpath", ".//span[@class='contact-channel']")
    CONTACT_PHONE = ("xpath", ".//span[@class='contact-phone']")
    
    # Действия с контактом
    EDIT_CONTACT_BUTTON = ("xpath", ".//button[contains(@class, 'edit-btn')]")
    DELETE_CONTACT_BUTTON = ("xpath", ".//button[contains(@class, 'info__btn_delete')]")
    ARCHIVE_CONTACT_BUTTON = ("xpath", ".//button[contains(@class, 'info__btn_archive')]")
    SEND_MESSAGE_BUTTON = ("xpath", ".//button[contains(@class, 'send-message-btn')]")
    
    # Модальные окна
    CONFIRM_DELETE_BUTTON = ("xpath", "//button[contains(text(), 'Ок')]")
    CONFIRM_ARCHIVE_BUTTON = ("xpath", "//button[@class, 'btn btn_primary btn_default btn_icon-none notification_button']")
    BUTTON_OK = ("xpath", "//button[@type, 'button']")
    BUTTON_OK2 = ("xpath", "//div[@class, 'notification_button-block']")
    CANCEL_DELETE_BUTTON = ("xpath", "//button[contains(text(), 'Отмена')]")
    
    # Выгрузка файлов
    EXPORT_BUTTON =  ("xpath", "//a[@class='load-contacts-ref']")
    EXPORT_EXCEL_BUTTON = ("xpath", "//button[contains(text(), 'Excel')]")
    EXPORT_CSV_BUTTON = ("xpath", "//button[contains(text(), 'CSV')]")
    
    # Сообщения
    SUCCESS_MESSAGE = ("xpath", "//div[contains(@class, 'success-message')]")
    ERROR_MESSAGE = ("xpath", "//div[contains(@class, 'error-message')]")
    
    # Форма редактирования
    EDIT_NAME_FIELD = ("xpath", "//input[@id='editContactName']")
    EDIT_LOGIN_FIELD = ("xpath", "//input[@id='editContactLogin']")
    EDIT_PHONE_FIELD = ("xpath", "//input[@id='editContactPhone']")
    EDIT_CHANNEL_SELECT = ("xpath", "//select[@id='editChannel']")
    UPDATE_CONTACT_BUTTON = ("xpath", "//button[contains(text(), 'Обновить')]")
    
    # Форма отправки сообщения
    MESSAGE_INPUT = ("xpath", "//textarea[@id='messageInput']")
    SEND_MESSAGE_MODAL_BUTTON = ("xpath", "//button[contains(text(), 'Отправить сообщение')]")
    
    @allure.step('Открытие страницы контактов')
    def open_contacts_page(self):
        """Открыть страницу контактов"""
        self.element_in_clickable(self.RAZV_BUTTON).click()
        self.element_in_clickable(self.CONTACTS_MENU).click()
        sleep(2)
    
    @allure.step('Открытие формы создания контакта')
    def open_add_contact_form(self):
        """Открыть форму создания контакта"""
        self.element_in_clickable(self.ADD_CONTACT_BUTTON).click()
        sleep(1)
    
    @allure.step('Выбор канала связи')
    def select_channel(self, channel):
        """Выбрать канал связи"""
        self.element_in_clickable(self.CHANNEL_SELECT_OPEN).click()
        self.element_in_clickable(self.CHANNEL_SELECT).click()
        sleep(3)
        # channel_options = {
        #     'telegram': self.CHANNEL_OPTION_TELEGRAM,
        #     'whatsapp': self.CHANNEL_OPTION_WHATSAPP,
        #     'viber': self.CHANNEL_OPTION_VIBER,
        #     'sms': self.CHANNEL_OPTION_SMS
        # }
        
        # if channel.lower() in channel_options:
        #     self.element_in_clickable(channel_options[channel.lower()]).click()
        # else:
        #     raise ValueError(f"Неподдерживаемый канал: {channel}")
        
        # return self
    
    @allure.step('Ввод имени контакта')
    def enter_contact_name(self, name):
        """Ввести имя контакта"""
        self.element_in_localed(self.NAME_FIELD).clear()
        self.element_in_localed(self.NAME_FIELD).send_keys(name)
        return self
    
    @allure.step('Ввод логина контакта')
    def enter_contact_login(self, login):
        """Ввести логин контакта"""
        self.element_in_localed(self.LOGIN_FIELD).clear()
        self.element_in_localed(self.LOGIN_FIELD).send_keys(login)
        return self
    
    @allure.step('Ввод телефона контакта')
    def enter_contact_phone(self, phone):
        """Ввести телефон контакта"""
        self.element_in_localed(self.PHONE_FIELD).clear()
        self.element_in_localed(self.PHONE_FIELD).send_keys(phone)
        return self
    
    @allure.step('Ввод текста сообщения')
    def enter_contact_message(self, message):
        """Ввести текст сообщения"""
        self.element_in_localed(self.MESSAGE_FIELD).clear()
        self.element_in_localed(self.MESSAGE_FIELD).send_keys(message)
        return self
    
    @allure.step('Создание контакта')
    def create_contact(self, channel, name, login, phone, message=""):
        """Создать контакт с полными данными"""
        self.open_add_contact_form()
        self.select_channel(channel)
        self.enter_contact_name(name)
        self.enter_contact_login(login)
        self.enter_contact_phone(phone)
        if message:
            self.enter_contact_message(message)
        self.element_in_clickable(self.SAVE_CONTACT_BUTTON).click()
        sleep(2)
        return self
    
    @allure.step('Отмена создания контакта')
    def cancel_create_contact(self):
        """Отменить создание контакта"""
        # Закрываем форму создания контакта
        self.close_modal_window('auto')
        sleep(1)
        return self
    
    @allure.step('Поиск контакта')
    def search_contact(self, search_term):
        """Поиск контакта по имени, логину или телефону"""
        self.element_in_localed(self.SEARCH_FIELD).clear()
        self.element_in_localed(self.SEARCH_FIELD).send_keys(search_term)
        #self.element_in_clickable(self.SEARCH_BUTTON).click()
        sleep(2)
        return self
    
    @allure.step('Фильтрация по каналу')
    def filter_by_channel(self, channel):
        """Фильтрация контактов по каналу"""
        self.element_in_clickable(self.CHANNEL_FILTER).click()
        # self.element_in_clickable(self.CHANNEL_FILTER_SELECT).click()
        # self.element_in_clickable(self.CHANNEL_OPTION_INSTAGRAM).click()
        channel_options = {
            # 'all': self.CHANNEL_OPTION_ALL,
            'instagram': self.CHANNEL_OPTION_INSTAGRAM,
            'telegram': self.CHANNEL_OPTION_TELEGRAM
            # 'whatsapp': self.CHANNEL_OPTION_WHATSAPP,
            # 'viber': self.CHANNEL_OPTION_VIBER,
            # 'sms': self.CHANNEL_OPTION_SMS
        }
        
        if channel.lower() in channel_options:
            self.element_in_clickable(channel_options[channel.lower()]).click()
        
        # self.element_in_clickable(self.CHANNEL_FILTER_SELECT).click()
        # # self.element_in_clickable(self.FILTER_BUTTON_SELECT).click()
        sleep(2)
        return self
    
    @allure.step('Очистка фильтров')
    def clear_filters(self):
        """Очистить все фильтры"""
        self.element_in_clickable(self.CLEAR_FILTER_BUTTON).click()
        sleep(1)
        return self
    
    @allure.step('Выгрузка контактов в Excel')
    def export_contacts_excel(self):
        """Выгрузить контакты в Excel"""
        # self.element_in_clickable(self.EXPORT_BUTTON).click()
        self.element_in_clickable(self.EXPORT_EXCEL_BUTTON).click()

        #urllib.request.urlopen(f)
        # urllib.request.urlopen(self.element_in_clickable(self.EXPORT_EXCEL_BUTTON).click())
        # print(group)
        sleep(3)
        return self
    
    @allure.step('Выгрузка контактов в CSV')
    def export_contacts_csv(self):
        """Выгрузить контакты в CSV"""
        self.element_in_clickable(self.EXPORT_BUTTON).click()
        self.element_in_clickable(self.EXPORT_CSV_BUTTON).click()
        sleep(3)
        return self
    
    @allure.step('Редактирование контакта')
    def edit_contact(self, contact_name, new_channel=None, new_name=None, new_login=None, new_phone=None):
        """Редактировать контакт"""
        # Найти контакт по имени
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.EDIT_CONTACT_BUTTON).click()
            sleep(1)
            
            if new_channel:
                self.element_in_clickable(self.EDIT_CHANNEL_SELECT).click()
                self.select_channel(new_channel)
            
            if new_name:
                self.element_in_localed(self.EDIT_NAME_FIELD).clear()
                self.element_in_localed(self.EDIT_NAME_FIELD).send_keys(new_name)
            
            if new_login:
                self.element_in_localed(self.EDIT_LOGIN_FIELD).clear()
                self.element_in_localed(self.EDIT_LOGIN_FIELD).send_keys(new_login)
            
            if new_phone:
                self.element_in_localed(self.EDIT_PHONE_FIELD).clear()
                self.element_in_localed(self.EDIT_PHONE_FIELD).send_keys(new_phone)
            
            self.element_in_clickable(self.UPDATE_CONTACT_BUTTON).click()
            sleep(2)
        
        return self
    
    @allure.step('Отмена редактирования контакта')
    def cancel_edit_contact(self, contact_name):
        """Отменить редактирование контакта"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.EDIT_CONTACT_BUTTON).click()
            sleep(1)
            # Закрываем форму редактирования
            self.close_modal_window('auto')
            sleep(1)
        return self
    
    @allure.step('Удаление контакта')
    def delete_contact(self, contact_name):
        """Удалить контакт"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.DELETE_CONTACT_BUTTON).click()
            sleep(1)
            # Подтверждаем удаление
            self.element_in_clickable(self.CONFIRM_DELETE_BUTTON).click()
            sleep(2)
        return self
    
    @allure.step('Архивация контакта')
    def archive_contact(self, contact_name):
        """Архивировать контакт"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.CONTACT_NAME_INSTAGRAM).click()
            sleep(1)
            self.element_in_clickable(self.ARCHIVE_CONTACT_BUTTON).click()
            sleep(1)
            # Подтверждаем архивацию
            # self.element_in_clickable(self.BUTTON_OK2).click()
            # self.element_in_clickable(self.CONFIRM_ARCHIVE_BUTTON).click()
            sleep(3)
            # self.close_modal_window('cancel')
            # sleep(1)
                        # Закрываем через JavaScript
            self.browser.execute_script("""
                // Закрываем окно архивации
document.querySelector("button[class='btn btn_primary btn_default btn_icon-none notification_button']").click()
                });
            """)
        
        return self
    
    @allure.step('Отмена архивации контакта')
    def cancel_archive_contact(self, contact_name):
        """Отменить архивацию контакта"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.CONTACT_NAME_INSTAGRAM).click()
            sleep(1)
            self.element_in_clickable(self.ARCHIVE_CONTACT_BUTTON).click()
            sleep(1)
            # Отменяем архивацию
            self.close_modal_window('cancel')
            sleep(1)
        return self
    
    @allure.step('Отправка сообщения контакту')
    def send_message_to_contact(self, contact_name, message):
        """Отправить сообщение контакту"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.SEND_MESSAGE_BUTTON).click()
            sleep(1)
            self.element_in_localed(self.MESSAGE_INPUT).clear()
            self.element_in_localed(self.MESSAGE_INPUT).send_keys(message)
            self.element_in_clickable(self.SEND_MESSAGE_MODAL_BUTTON).click()
            sleep(2)
        return self
    
    def find_contact_by_name(self, name):
        """Найти контакт по имени"""
        try:
            contacts = self.elements_in_visible(self.CONTACT_NAME_INSTAGRAM)
            for contact in contacts:
                contact_name_element = contact.find_element(*self.CONTACT_NAME_INSTAGRAM)
                if contact_name_element.text == name:
                    return contact
        except:
            pass
        return None
    
    def get_contact_info(self, contact_name):
        """Получить информацию о контакте"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            try:
                name = contact_item.find_element(*self.CONTACT_NAME).text
                channel = contact_item.find_element(*self.CONTACT_CHANNEL).text
                phone = contact_item.find_element(*self.CONTACT_PHONE).text
                return {
                    'name': name,
                    'channel': channel,
                    'phone': phone
                }
            except:
                pass
        return None
    
    def is_contact_exists(self, contact_name):
        """Проверить существование контакта"""
        return self.find_contact_by_name(contact_name) is not None
    
    def get_contacts_count(self):
        """Получить количество контактов"""
        try:
            contacts = self.elements_in_visible(self.CONTACT_ITEM)
            return len(contacts)
        except:
            return 0
    
    def is_success_message_displayed(self):
        """Проверить отображение сообщения об успехе"""
        try:
            success_message = self.element_in_visible(self.SUCCESS_MESSAGE, timeout=5)
            return success_message.is_displayed()
        except:
            return False
    
    def get_success_message_text(self):
        """Получить текст сообщения об успехе"""
        try:
            success_message = self.element_in_visible(self.SUCCESS_MESSAGE, timeout=5)
            return success_message.text
        except:
            return ""
    
    def is_error_message_displayed(self):
        """Проверить отображение сообщения об ошибке"""
        try:
            error_message = self.element_in_visible(self.ERROR_MESSAGE, timeout=5)
            return error_message.is_displayed()
        except:
            return False
    
    def get_error_message_text(self):
        """Получить текст сообщения об ошибке"""
        try:
            error_message = self.element_in_visible(self.ERROR_MESSAGE, timeout=5)
            return error_message.text
        except:
            return ""
    
    @allure.step('Скачивание Excel файла с контактами')
    def download_excel_file(self, download_dir=None):
        """Скачать Excel файл с контактами"""
        if download_dir is None:
            download_dir = os.path.join(os.getcwd(), "downloads")
        
        # Создаем папку для загрузок если её нет
        os.makedirs(download_dir, exist_ok=True)
        
        # Настраиваем опции браузера для загрузки файлов
        self.browser.execute_cdp_cmd('Page.setDownloadBehavior', {
            'behavior': 'allow',
            'downloadPath': download_dir
        })
        
        # Получаем количество файлов до скачивания
        files_before = len([f for f in os.listdir(download_dir) if f.endswith('.xlsx')])
        
        try:
            # Проверяем, что кнопка экспорта видна и кликабельна
            export_button = self.element_in_clickable(self.EXPORT_BUTTON, timeout=15)
            
            # Прокручиваем к элементу если нужно
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_button)
            sleep(1)
            
            # Кликаем на кнопку экспорта Excel
            export_button.click()
            print("✅ Кнопка экспорта Excel нажата")
            
        except Exception as e:
            print(f"❌ Ошибка при клике на кнопку экспорта: {e}")
            # Попробуем альтернативный способ клика
            try:
                export_button = self.browser.find_element(*self.EXPORT_BUTTON)
                self.browser.execute_script("arguments[0].click();", export_button)
                print("✅ Кнопка экспорта Excel нажата через JavaScript")
            except Exception as e2:
                raise Exception(f"Не удалось нажать на кнопку экспорта Excel: {e2}")
        
        # Ждем скачивания файла с таймаутом
        max_wait_time = 30  # Максимальное время ожидания в секундах
        wait_interval = 1   # Интервал проверки в секундах
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            sleep(wait_interval)
            elapsed_time += wait_interval
            
            # Проверяем количество файлов после скачивания
            files_after = len([f for f in os.listdir(download_dir) if f.endswith('.csv')])
            
            if files_after > files_before:
                print(f"✅ Файл скачался за {elapsed_time} секунд")
                break
                
            print(f"⏳ Ожидание скачивания... {elapsed_time}/{max_wait_time} сек")
        else:
            raise Exception(f"Файл не скачался в течение {max_wait_time} секунд")
        
        # Находим самый новый Excel файл
        excel_files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]
        if not excel_files:
            raise Exception("Excel файлы не найдены в папке загрузок")
            
        latest_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(download_dir, x)))
        file_path = os.path.join(download_dir, latest_file)
        
        # Проверяем, что файл действительно скачался и не пустой
        if not os.path.exists(file_path):
            raise Exception(f"Файл не найден по пути: {file_path}")
            
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            raise Exception("Скачанный файл пустой")
            
        print(f"✅ Excel файл успешно скачан: {file_path} (размер: {file_size} байт)")
        
        return file_path
    
    @allure.step('Проверка содержимого Excel файла')
    def verify_excel_file_content(self, file_path, expected_columns=None):
        """Проверить содержимое Excel файла"""
        # try:
            # Читаем Excel файл
        #df = pd.read_excel(file_path)
        
        df = pd.read_csv(file_path)
            
            # Проверяем, что файл не пустой
        assert not df.empty, "Excel файл пустой"
            
            # Проверяем наличие ожидаемых колонок
            # if expected_columns:
            #     for column in expected_columns:
            #         assert column in df.columns, f"Колонка '{column}' не найдена в Excel файле"
            
            # # Выводим информацию о файле
            # print(f"✅ Excel файл содержит {len(df)} строк и {len(df.columns)} колонок")
            # print(f"📊 Колонки: {list(df.columns)}")
            
        return df
            
        # except Exception as e:
        #     assert False, f"Ошибка при чтении Excel файла: {str(e)}"
    
    @allure.step('Открытие Excel файла')
    def open_excel_file(self, file_path):
        """Открыть Excel файл в системе"""
        try:
            import subprocess
            import platform
            
            # Определяем команду для открытия файла в зависимости от ОС
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
            
            print(f"✅ Excel файл открыт: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при открытии файла: {str(e)}")
            return False
    
    @allure.step('Проверка доступности кнопки экспорта Excel')
    def is_export_button_available(self):
        """Проверить, доступна ли кнопка экспорта Excel"""
        try:
            # Проверяем, что кнопка видна
            self.element_in_visible(self.EXPORT_BUTTON, timeout=5)
            # Проверяем, что кнопка кликабельна
            self.element_in_clickable(self.EXPORT_BUTTON, timeout=5)
            return True
        except:
            return False
    
    @allure.step('Полная проверка экспорта Excel')
    def test_excel_export_complete(self, download_dir=None, expected_columns=None):
        """Полный тест экспорта Excel файла"""
        # Проверяем доступность кнопки перед скачиванием
        if not self.is_export_button_available():
            raise Exception("Кнопка экспорта Excel недоступна")
        
        # Скачиваем файл
        file_path = self.download_excel_file(download_dir)
        
        # Проверяем содержимое
        df = self.verify_excel_file_content(file_path, expected_columns)
        
        # Открываем файл
        self.open_excel_file(file_path)
        
        return file_path, df
    
    @allure.step('Закрытие модального окна')
    def close_modal_window(self, method='close_button'):
        """
        Закрыть модальное окно различными способами
        
        Args:
            method (str): Способ закрытия модального окна
                - 'close_button': Клик по кнопке закрытия (X)
                - 'escape': Нажатие клавиши Escape
                - 'overlay': Клик по фону модального окна
                - 'cancel': Клик по кнопке "Отмена" или "Cancel"
                - 'auto': Автоматический поиск любого способа закрытия
        """
        try:
            if method == 'close_button':
                # Ищем кнопку закрытия (X)
                close_buttons = [
                    self.MODAL_CLOSE_BUTTON,
                    ("xpath", "//button[@aria-label='Close']"),
                    ("xpath", "//button[contains(@class, 'close')]"),
                    ("xpath", "//span[contains(@class, 'close')]"),
                    ("xpath", "//i[contains(@class, 'close')]"),
                    ("xpath", "//button[contains(text(), '×')]"),
                    ("xpath", "//button[contains(text(), '✕')]")
                ]
                
                for button_locator in close_buttons:
                    try:
                        close_button = self.element_in_clickable(button_locator, timeout=3)
                        close_button.click()
                        print(f"✅ Модальное окно закрыто кнопкой: {button_locator[1]}")
                        sleep(1)
                        return True
                    except:
                        continue
                        
            elif method == 'escape':
                # Нажимаем клавишу Escape
                from selenium.webdriver.common.keys import Keys
                self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                print("✅ Модальное окно закрыто клавишей Escape")
                sleep(1)
                return True
                
            elif method == 'overlay':
                # Кликаем по фону модального окна
                try:
                    overlay = self.element_in_clickable(self.MODAL_OVERLAY, timeout=3)
                    overlay.click()
                    print("✅ Модальное окно закрыто кликом по фону")
                    sleep(1)
                    return True
                except:
                    # Альтернативный способ - клик по координатам
                    self.browser.execute_script("document.querySelector('.modal-backdrop').click();")
                    print("✅ Модальное окно закрыто кликом по фону (JavaScript)")
                    sleep(1)
                    return True
                    
            elif method == 'cancel':
                # Ищем кнопку "Отмена" или "Cancel"
                cancel_buttons = [
                    self.CANCEL_DELETE_BUTTON,
                    ("xpath", "//button[contains(text(), 'Отмена')]"),
                    ("xpath", "//button[contains(text(), 'Cancel')]"),
                    ("xpath", "//button[contains(text(), 'Нет')]"),
                    ("xpath", "//button[contains(text(), 'No')]")
                ]
                
                for button_locator in cancel_buttons:
                    try:
                        cancel_button = self.element_in_clickable(button_locator, timeout=3)
                        cancel_button.click()
                        print(f"✅ Модальное окно закрыто кнопкой отмены: {button_locator[1]}")
                        sleep(1)
                        return True
                    except:
                        continue
                        
            elif method == 'auto':
                # Автоматический поиск любого способа закрытия
                methods_to_try = ['close_button', 'escape', 'overlay', 'cancel']
                for method_name in methods_to_try:
                    if self.close_modal_window(method_name):
                        return True
                        
        except Exception as e:
            print(f"❌ Ошибка при закрытии модального окна методом '{method}': {e}")
            
        return False
    
    @allure.step('Проверка наличия модального окна')
    def is_modal_window_open(self):
        """Проверить, открыто ли модальное окно"""
        try:
            # Проверяем наличие модального контейнера
            modal_container = self.element_in_visible(self.MODAL_CONTAINER, timeout=2)
            return modal_container.is_displayed()
        except:
            try:
                # Альтернативная проверка через JavaScript
                is_modal_open = self.browser.execute_script("""
                    return document.querySelector('.modal') !== null || 
                           document.querySelector('.popup') !== null ||
                           document.querySelector('[role="dialog"]') !== null;
                """)
                return is_modal_open
            except:
                return False
    
    @allure.step('Принудительное закрытие всех модальных окон')
    def force_close_all_modals(self):
        """Принудительно закрыть все модальные окна"""
        try:
            # Закрываем через JavaScript
            self.browser.execute_script("""
                // Закрываем все модальные окна
                document.querySelectorAll('.modal').forEach(modal => {
                    modal.style.display = 'none';
                    modal.classList.remove('show');
                });
                
                // Удаляем backdrop
                document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
                    backdrop.remove();
                });
                
                // Удаляем класс modal-open с body
                document.body.classList.remove('modal-open');
            """)
            print("✅ Все модальные окна принудительно закрыты через JavaScript")
            sleep(1)
            return True
        except Exception as e:
            print(f"❌ Ошибка при принудительном закрытии модальных окон: {e}")
            return False

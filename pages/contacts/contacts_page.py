"""
Страница управления контактами
"""
from time import sleep
import allure
from pages.base_page import BasePage


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
    CHANNEL_OPTION_TELEGRAM = ("xpath", "//option[@value='telegram']")
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
    CHANNEL_FILTER = ("xpath", "//select[@id='channelFilter']")
    FILTER_BUTTON = ("xpath", "//button[contains(text(), 'Фильтровать')]")
    CLEAR_FILTER_BUTTON = ("xpath", "//button[contains(text(), 'Очистить фильтры')]")
    
    # Список контактов
    CONTACTS_LIST = ("xpath", "//div[@class='contacts-list']")
    CONTACT_ITEM = ("xpath", "//p[@class='contact-card__username']")
    CONTACT_NAME = ("xpath", "//p[@class='contact-card__username']")
    CONTACT_CHANNEL = ("xpath", ".//span[@class='contact-channel']")
    CONTACT_PHONE = ("xpath", ".//span[@class='contact-phone']")
    
    # Действия с контактом
    EDIT_CONTACT_BUTTON = ("xpath", ".//button[contains(@class, 'edit-btn')]")
    DELETE_CONTACT_BUTTON = ("xpath", ".//button[contains(@class, 'delete-btn')]")
    ARCHIVE_CONTACT_BUTTON = ("xpath", ".//button[contains(@class, 'archive-btn')]")
    SEND_MESSAGE_BUTTON = ("xpath", ".//button[contains(@class, 'send-message-btn')]")
    
    # Модальные окна
    CONFIRM_DELETE_BUTTON = ("xpath", "//button[contains(text(), 'Удалить')]")
    CONFIRM_ARCHIVE_BUTTON = ("xpath", "//button[contains(text(), 'Архивировать')]")
    CANCEL_DELETE_BUTTON = ("xpath", "//button[contains(text(), 'Отмена')]")
    
    # Выгрузка файлов
    EXPORT_BUTTON = ("xpath", "//button[contains(text(), 'Выгрузить')]")
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
        
        channel_options = {
            'telegram': self.CHANNEL_OPTION_TELEGRAM,
            'whatsapp': self.CHANNEL_OPTION_WHATSAPP,
            'viber': self.CHANNEL_OPTION_VIBER,
            'sms': self.CHANNEL_OPTION_SMS
        }
        
        if channel.lower() in channel_options:
            self.element_in_clickable(channel_options[channel.lower()]).click()
        
        self.element_in_clickable(self.FILTER_BUTTON).click()
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
        self.element_in_clickable(self.EXPORT_BUTTON).click()
        self.element_in_clickable(self.EXPORT_EXCEL_BUTTON).click()
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
    
    @allure.step('Удаление контакта')
    def delete_contact(self, contact_name):
        """Удалить контакт"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.DELETE_CONTACT_BUTTON).click()
            sleep(1)
            self.element_in_clickable(self.CONFIRM_DELETE_BUTTON).click()
            sleep(2)
        return self
    
    @allure.step('Архивация контакта')
    def archive_contact(self, contact_name):
        """Архивировать контакт"""
        contact_item = self.find_contact_by_name(contact_name)
        if contact_item:
            self.element_in_clickable(self.ARCHIVE_CONTACT_BUTTON).click()
            sleep(1)
            self.element_in_clickable(self.CONFIRM_ARCHIVE_BUTTON).click()
            sleep(2)
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
            contacts = self.elements_in_visible(self.CONTACT_ITEM)
            for contact in contacts:
                contact_name_element = contact.find_element(*self.CONTACT_NAME)
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

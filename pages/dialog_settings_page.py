from time import sleep
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.links import Links
from pages.base_page import BasePage


class DialogSettingsPage(BasePage):
    # Константы класса
    PAGE_URL = Links.DIALOG_SETTINGS_URL
    
    # Локаторы элементов страницы настроек диалога
    
    # Основные элементы навигации
    DIALOG_SETTINGS_TITLE = (
        "xpath", 
        "//h2[contains(text(),'Настройки диалога')]"
    )
    
    # Локаторы для настройки "Оставлять сообщения непрочитанными"
    LEAVE_MESSAGES_UNREAD_TOGGLE = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Оставлять сообщения непрочитанными')]]//button[contains(@class,'switch')]"
    )
    LEAVE_MESSAGES_UNREAD_PARENT = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Оставлять сообщения непрочитанными')]]"
    )
    
    # Локаторы для настройки "Присвоение даты контакта"
    ASSIGN_CONTACT_DATE_TOGGLE = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Присвоение даты контакта')]]//button[contains(@class,'switch')]"
    )
    ASSIGN_CONTACT_DATE_PARENT = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Присвоение даты контакта')]]"
    )
    
    # Локаторы для настройки "Отметка диалогов без ответа менеджера"
    MARK_DIALOGS_NO_MANAGER_RESPONSE_TOGGLE = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Отметка диалогов без ответа менеджера')]]//button[contains(@class,'switch')]"
    )
    MARK_DIALOGS_NO_MANAGER_RESPONSE_PARENT = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Отметка диалогов без ответа менеджера')]]"
    )
    
    # Локаторы для настройки "Включить уведомления о истечении времени ответа"
    ENABLE_RESPONSE_TIME_NOTIFICATIONS_TOGGLE = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Включить уведомления о истечении времени ответа')]]//button[contains(@class,'switch')]"
    )
    ENABLE_RESPONSE_TIME_NOTIFICATIONS_PARENT = (
        "xpath", 
        "//div[contains(@class,'setting-item') and .//text()[contains(.,'Включить уведомления о истечении времени ответа')]]"
    )
    
    # Кнопка настройки таймера отметки
    SETUP_TIMER_BUTTON = (
        "xpath", 
        "//button[contains(@class,'btn_primary btn_small btn_icon-none time-without-answer-setting__btn') and contains(.,'Настроить таймер отметки')]"
    )
    
    # Кнопка сохранения настроек (может отсутствовать при автосохранении)
    SAVE_SETTINGS_BUTTON = (
        "xpath", 
        "//button[@type='button' and contains(text(),'Сохранить')]"
    )


    @allure.step("Открытие страницы настроек диалога")
    def open_dialog_settings(self):
        self.open()
        return self.element_in_visible(self.DIALOG_SETTINGS_TITLE)

    @allure.step("Переход к настройкам диалога")
    def go_to_dialog_settings(self):
        return self.open_dialog_settings()

    @allure.step("Нажатие на кнопку 'Настроить таймер отметки'")
    def click_setup_timer_button(self):
        self.element_in_clickable(self.SETUP_TIMER_BUTTON).click()

    @allure.step("Нажатие на кнопку сохранения настроек")
    def click_save_settings_button(self):
        self.element_in_clickable(self.SAVE_SETTINGS_BUTTON).click()
        self.browser.refresh()


    # ========== УНИВЕРСАЛЬНЫЕ МЕТОДЫ ==========

    @allure.step("Нажатие на переключатель настройки: {setting_name}")
    def click_toggle_setting(self, setting_name, toggle_locator):
        self.element_in_clickable(toggle_locator).click()

    @allure.step("Проверка и активация элемента: {element_name}")
    def check_and_activate_element(self, element_name, toggle_locator):
        """
        Универсальный метод для проверки и активации любого элемента.
        
        Args:
            element_name (str): Название элемента для логирования
            toggle_locator (tuple): Локатор кнопки переключения
        """
        try:
            element = self.element_in_visible(toggle_locator)
            
            # Получаем атрибут class элемента
            class_attribute = element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            if "switch_active" in class_attribute:
                print(f"{element_name} уже активен")
            else:
                print(f"{element_name} неактивен, активируем его")
                self.element_in_clickable(toggle_locator).click()
                sleep(1)
                print(f"{element_name} активирован")
        except Exception as e:
            print(f"Ошибка при проверке/активации {element_name}: {str(e)}")
            raise

    
    @allure.step("Проверка и деактивация элемента: {element_name}")
    def check_and_deactivate_element(self, element_name, toggle_locator):
        """
        Универсальный метод для проверки и деактивации любого элемента.
        
        Args:
            element_name (str): Название элемента для логирования
            toggle_locator (tuple): Локатор кнопки переключения
        """
        try:
            element = self.element_in_visible(toggle_locator)
            
            # Получаем атрибут class элемента
            class_attribute = element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            if "switch_active" not in class_attribute:
                print(f"{element_name} уже неактивен")
            else:
                print(f"{element_name} активен, деактивируем его")
                self.element_in_clickable(toggle_locator).click()
                sleep(1)
                print(f"{element_name} деактивирован")
        except Exception as e:
            print(f"Ошибка при проверке/деактивации {element_name}: {str(e)}")
            raise

    @allure.step("Проверка что элемент активирован: {element_name}")
    def check_element_is_active(self, element_name, toggle_locator):
        """
        Универсальный метод для проверки что элемент активирован.
        
        Args:
            element_name (str): Название элемента для логирования
            toggle_locator (tuple): Локатор кнопки переключения
        """
        try:
            element = self.element_in_visible(toggle_locator)
            class_attribute = element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            # Проверяем, содержит ли класс 'switch_active'
            if "switch_active" in class_attribute:
                print(f"{element_name} активен - проверка пройдена")
                assert True
            else:
                print(f"{element_name} неактивен - проверка не пройдена")
                assert False
        except Exception as e:
            print(f"Ошибка при проверке {element_name}: {str(e)}")
            assert False

    @allure.step("Проверка что элемент деактивирован: {element_name}")
    def check_element_is_inactive(self, element_name, toggle_locator):
        """ 
        Универсальный метод для проверки что элемент деактивирован.
        
        Args:
            element_name (str): Название элемента для логирования
            toggle_locator (tuple): Локатор кнопки переключения
        """
        try:
            element = self.element_in_visible(toggle_locator)
            class_attribute = element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            if "switch_active" not in class_attribute:
                print(f"{element_name} неактивен - проверка пройдена")
                assert True
            else:
                print(f"{element_name} активен - проверка не пройдена")
                assert False
        except Exception as e:
            print(f"Ошибка при проверке {element_name}: {str(e)}")
            assert False

    # ========== МЕТОДЫ-ОБЕРТКИ ДЛЯ настройки "Оставлять сообщения непрочитанными" ==========

    @allure.step("Проверка и активация настройки 'Оставлять сообщения непрочитанными'")
    def check_and_activate_leave_messages_unread(self):
        return self.check_and_activate_element(
            "Оставлять сообщения непрочитанными",
            self.LEAVE_MESSAGES_UNREAD_TOGGLE
        )

    @allure.step("Проверка и деактивация настройки 'Оставлять сообщения непрочитанными'")
    def check_and_deactivate_leave_messages_unread(self):
        return self.check_and_deactivate_element(
            "Оставлять сообщения непрочитанными",
            self.LEAVE_MESSAGES_UNREAD_TOGGLE
        )

    @allure.step("Проверка что настройка 'Оставлять сообщения непрочитанными' активирована")
    def check_activate_leave_messages_unread(self):
        return self.check_element_is_active(
            "Оставлять сообщения непрочитанными",
            self.LEAVE_MESSAGES_UNREAD_TOGGLE
        )
        
    @allure.step("Проверка что настройка 'Оставлять сообщения непрочитанными' деактивирована")
    def check_deactivate_leave_messages_unread(self):
        return self.check_element_is_inactive(
            "Оставлять сообщения непрочитанными",
            self.LEAVE_MESSAGES_UNREAD_TOGGLE
        )
        
    # ========== МЕТОДЫ-ОБЕРТКИ ДЛЯ настройки "Присвоение даты контакта" ==========

    @allure.step("Проверка и активация настройки 'Присвоение даты контакта'")
    def check_and_activate_assign_contact_date(self):
        """Проверяет и активирует настройку 'Присвоение даты контакта'."""
        return self.check_and_activate_element(
            "Присвоение даты контакта", 
            self.ASSIGN_CONTACT_DATE_TOGGLE
        )           

    @allure.step("Проверка и деактивация настройки 'Присвоение даты контакта'")
    def check_and_deactivate_assign_contact_date(self):
        """Проверяет и деактивирует настройку 'Присвоение даты контакта'."""
        return self.check_and_deactivate_element(
            "Присвоение даты контакта", 
            self.ASSIGN_CONTACT_DATE_TOGGLE
        )           

    @allure.step("Проверка что настройка 'Присвоение даты контакта' активирована")
    def check_activate_assign_contact_date(self):
        """Проверяет что настройка 'Присвоение даты контакта' активирована."""
        return self.check_element_is_active(
            "Присвоение даты контакта", 
            self.ASSIGN_CONTACT_DATE_TOGGLE
        )           

    @allure.step("Проверка что настройка 'Присвоение даты контакта' деактивирована")
    def check_deactivate_assign_contact_date(self):
        """Проверяет что настройка 'Присвоение даты контакта' деактивирована."""
        return self.check_element_is_inactive(
            "Присвоение даты контакта", 
            self.ASSIGN_CONTACT_DATE_TOGGLE
        )           


        
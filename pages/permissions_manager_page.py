from time import sleep

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.links import Links
from pages.base_page import BasePage


class PermissionsManagerPage(BasePage):
    # Константы класса
    PAGE_URL = Links.PERMISSIONS_MANAGER_URL
    
    # Локаторы элементов страницы
    MANAGER_PAGE_BUTTON = (
        "xpath", 
        "//div[@class='navbar-icon-section']/span[contains(text(),'Менеджеры')]"
    )
    MANAGER = (
        "xpath", 
        "//p[contains(@class,'manager-card__email') and contains(text(),'manager-avto@mail.ru')]"
    )
    PERMISSIONS_BUTTON = (
        "xpath", 
        "//button[contains(@class,'manager-mainbar-page-button') and contains(text(),'Разрешения')]"
    )
    
    # Локаторы для тестового тега 1
    TEST_TEG_1 = (
        "xpath", 
        "//span[normalize-space(.)='Тестовый тег 1']/following-sibling::div[contains(@class,'manager-permission-controller')]//div[contains(@class,'manager-permission-toggle-button')]"
    )
    TEST_TEG_1_PARENT = (
        "xpath", 
        "//span[normalize-space(.)='Тестовый тег 1']/following-sibling::div[contains(@class,'manager-permission-controller')]"
    )
    
     # Локаторы для тестового статуса 1
    TEST_STATUS_1 = (
        "xpath", 
        "//span[normalize-space(.)='Тестовый статус 1']/following-sibling::div[contains(@class,'manager-permission-controller')]//div[contains(@class,'manager-permission-toggle-button')]"
    )
    TEST_STATUS_1_PARENT = (
        "xpath", 
        "//span[normalize-space(.)='Тестовый статус 1']/following-sibling::div[contains(@class,'manager-permission-controller')]"
    )

    # Локаторы для разрешений диалогов
    SAVE_DIALOG_ACCESS = (
        "xpath", 
        "//p[contains(text(),'Сохранить доступ к диалогам')]/following-sibling::button//div[contains(@class,'manager-permission-toggle-button')]"
    )
    SAVE_DIALOG_ACCESS_PARENT = (
        "xpath", 
        "//p[contains(text(),'Сохранить доступ к диалогам')]/following-sibling::button"
    )
    
    EDIT_DIALOG_INFO = (
        "xpath", 
        "//p[contains(text(),'Возможность редактировать информацию')]/following-sibling::button//div[contains(@class,'manager-permission-toggle-button')]"
    )
    EDIT_DIALOG_INFO_PARENT = (
        "xpath", 
        "//p[contains(text(),'Возможность редактировать информацию')]/following-sibling::button"
    )
    
    VIEW_CONTACT_INFO = (
        "xpath", 
        "//p[contains(text(),'Просмотр контактной информации')]/following-sibling::button//div[contains(@class,'manager-permission-toggle-button')]"
    )
    VIEW_CONTACT_INFO_PARENT = (
        "xpath", 
        "//p[contains(text(),'Просмотр контактной информации')]/following-sibling::button"
    )
    
    EXPORT_CONTACTS = (
        "xpath", 
        "//p[contains(text(),'Разрешить менеджеру выгружать')]/following-sibling::button//div[contains(@class,'manager-permission-toggle-button')]"
    )
    EXPORT_CONTACTS_PARENT = (
        "xpath", 
        "//p[contains(text(),'Разрешить менеджеру выгружать')]/following-sibling::button"
    )

    # Кнопка сохранения
    BUTTON_SAVE = ("xpath", "//button[@type='button' and text()='Сохранить']")


    @allure.step("Нажатие на кнопку страницы менеджера")
    def click_manager_page_button(self):
        self.element_in_visible(self.MANAGER_PAGE_BUTTON).click()


    @allure.step("Нажатие на менеджера") 
    def click_manager(self):
        self.element_in_clickable(self.MANAGER).click()


    @allure.step("Нажатие на кнопку разрешений")
    def click_permissions_button(self):
        self.element_in_clickable(self.PERMISSIONS_BUTTON).click()


    @allure.step("Переход к разрешениям менеджера")
    def go_to_manager_permissions(self):
        """Объединенный метод: нажимает на менеджера и затем на кнопку разрешений."""
        self.click_manager()
        self.click_permissions_button()


    @allure.step("Нажатие на кнопку сохранения разрешений")
    def click_save_button(self):
        self.element_in_clickable(self.BUTTON_SAVE).click()
        self.browser.refresh()


    # ========== УНИВЕРСАЛЬНЫЕ МЕТОДЫ ==========

    @allure.step("Нажатие на переключатель элемента: {element_name}")
    def click_toggle_element(self, element_name, toggle_locator):
        """Универсальный метод для нажатия на переключатель любого элемента."""
        self.element_in_clickable(toggle_locator).click()


    @allure.step("Проверка и активация элемента: {element_name}")
    def check_and_activate_element(self, element_name, toggle_locator, parent_locator):
        """
        Универсальный метод для проверки и активации любого элемента.
        
        Args:
            element_name (str): Название элемента для логирования
            toggle_locator (tuple): Локатор кнопки переключения
            parent_locator (tuple): Локатор родительского элемента
        """
        try:
            # Находим родительский элемент
            parent_element = self.element_in_visible(parent_locator)
            
            # Получаем атрибут class родительского элемента
            class_attribute = parent_element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            # Проверяем, содержит ли класс 'active'
            if "active" in class_attribute:
                print(f"{element_name} уже активен")
                assert True
            else:
                print(f"{element_name} неактивен, активируем его")
                # Нажимаем на кнопку переключения
                self.element_in_clickable(toggle_locator).click()
                
                # Нажимаем кнопку сохранения
                self.click_save_button()
                
                # Возвращаемся к разрешениям после обновления страницы
                self.go_to_manager_permissions()
                
                # Проверяем результат
                updated_parent = self.element_in_visible(parent_locator)
                updated_class = updated_parent.get_attribute("class")
                
                if "active" in updated_class:
                    print(f"{element_name} успешно активирован")
                    assert True
                else:
                    print(f"Не удалось активировать {element_name}")
                    assert False
                    
        except Exception as e:
            print(f"Ошибка при проверке/активации {element_name}: {str(e)}")
            assert False


    @allure.step("Проверка и деактивация элемента: {element_name}")
    def check_and_deactivate_element(self, element_name, toggle_locator, parent_locator):
        """
        Универсальный метод для проверки и деактивации любого элемента.
        
        Args:
            element_name (str): Название элемента для логирования
            toggle_locator (tuple): Локатор кнопки переключения
            parent_locator (tuple): Локатор родительского элемента
        """
        try:
            # Находим родительский элемент
            parent_element = self.element_in_visible(parent_locator)
            
            # Получаем атрибут class родительского элемента
            class_attribute = parent_element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            # Проверяем, содержит ли класс 'active'
            if "active" not in class_attribute:
                print(f"{element_name} уже неактивен")
                assert True
            else:
                print(f"{element_name} активен, деактивируем его")
                # Нажимаем на кнопку переключения
                self.element_in_clickable(toggle_locator).click()
                
                # Нажимаем кнопку сохранения
                self.click_save_button()
                
                # Возвращаемся к разрешениям после обновления страницы
                self.go_to_manager_permissions()
                
                # Проверяем результат
                updated_parent = self.element_in_visible(parent_locator)
                updated_class = updated_parent.get_attribute("class")
                
                if "active" not in updated_class:
                    print(f"{element_name} успешно деактивирован")
                    assert True
                else:
                    print(f"Не удалось деактивировать {element_name}")
                    assert False
                    
        except Exception as e:
            print(f"Ошибка при проверке/деактивации {element_name}: {str(e)}")
            assert False


    @allure.step("Проверка что элемент активирован: {element_name}")
    def check_element_is_active(self, element_name, parent_locator):
        """
        Универсальный метод для проверки что элемент активирован.
        
        Args:
            element_name (str): Название элемента для логирования
            parent_locator (tuple): Локатор родительского элемента
        """
        try:
            # Находим родительский элемент
            parent_element = self.element_in_visible(parent_locator)
            
            # Получаем атрибут class родительского элемента
            class_attribute = parent_element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            # Проверяем, содержит ли класс 'active'
            if "active" in class_attribute:
                print(f"{element_name} активен - проверка пройдена")
                assert True
            else:
                print(f"{element_name} неактивен - проверка не пройдена")
                assert False
                
        except Exception as e:
            print(f"Ошибка при проверке {element_name}: {str(e)}")
            assert False


    @allure.step("Проверка что элемент деактивирован: {element_name}")
    def check_element_is_inactive(self, element_name, parent_locator):
        """
        Универсальный метод для проверки что элемент деактивирован.
        
        Args:
            element_name (str): Название элемента для логирования
            parent_locator (tuple): Локатор родительского элемента
        """
        try:
            # Находим родительский элемент
            parent_element = self.element_in_visible(parent_locator)
            
            # Получаем атрибут class родительского элемента
            class_attribute = parent_element.get_attribute("class")
            print(f"Текущие классы {element_name}: {class_attribute}")
            
            # Проверяем, содержит ли класс 'active'
            if "active" not in class_attribute:
                print(f"{element_name} неактивен - проверка пройдена")
                assert True
            else:
                print(f"{element_name} активен - проверка не пройдена")
                assert False
                
        except Exception as e:
            print(f"Ошибка при проверке {element_name}: {str(e)}")
            assert False

    # ========== МЕТОДЫ-ОБЕРТКИ ДЛЯ ТЕСТОВОГО ТЕГА 1 ==========

    @allure.step("Нажатие на переключатель тестового тега 1")
    def click_toggle_test_tag_1(self):
        """Нажимает на переключатель тестового тега 1."""
        return self.click_toggle_element("Тестовый тег 1", self.TEST_TEG_1)


    @allure.step("Проверка и активация тестового тега 1 если он не активен")
    def check_and_activate_test_tag_1(self):
        """Проверяет и активирует тестовый тег 1 при необходимости."""
        return self.check_and_activate_element(
            "Тестовый тег 1", 
            self.TEST_TEG_1, 
            self.TEST_TEG_1_PARENT
        )


    @allure.step("Проверка и деактивация тестового тега 1 если он активирован")
    def check_and_deactivate_test_tag_1(self):
        """Проверяет и деактивирует тестовый тег 1 при необходимости."""
        return self.check_and_deactivate_element(
            "Тестовый тег 1", 
            self.TEST_TEG_1, 
            self.TEST_TEG_1_PARENT
        )


    @allure.step("Проверка что тестовый тег 1 активирован")
    def check_activate_test_tag_1(self):
        """Проверяет что тестовый тег 1 активирован."""
        return self.check_element_is_active("Тестовый тег 1", self.TEST_TEG_1_PARENT)


    @allure.step("Проверка что тестовый тег 1 деактивирован")
    def check_deactivate_test_tag_1(self):
        """Проверяет что тестовый тег 1 деактивирован."""
        return self.check_element_is_inactive("Тестовый тег 1", self.TEST_TEG_1_PARENT)

    # ========== МЕТОДЫ-ОБЕРТКИ ДЛЯ ТЕСТОВОГО СТАТУСА 1 ==========

    @allure.step("Нажатие на переключатель тестового статуса 1")
    def click_toggle_test_status_1(self):
        """Нажимает на переключатель тестового статуса 1."""
        return self.click_toggle_element("Тестовый статус 1", self.TEST_STATUS_1)


    @allure.step("Проверка и активация тестового статуса 1 если он не активен")
    def check_and_activate_test_status_1(self):
        """Проверяет и активирует тестовый статус 1 при необходимости."""
        return self.check_and_activate_element(
            "Тестовый статус 1", 
            self.TEST_STATUS_1, 
            self.TEST_STATUS_1_PARENT
        )


    @allure.step("Проверка и деактивация тестового статуса 1 если он активирован")
    def check_and_deactivate_test_status_1(self):
        """Проверяет и деактивирует тестовый статус 1 при необходимости."""
        return self.check_and_deactivate_element(
            "Тестовый статус 1", 
            self.TEST_STATUS_1, 
            self.TEST_STATUS_1_PARENT
        )


    @allure.step("Проверка что тестовый статус 1 активирован")
    def check_activate_test_status_1(self):
        """Проверяет что тестовый статус 1 активирован."""
        return self.check_element_is_active("Тестовый статус 1", self.TEST_STATUS_1_PARENT)


    @allure.step("Проверка что тестовый статус 1 деактивирован")
    def check_deactivate_test_status_1(self):
        """Проверяет что тестовый статус 1 деактивирован."""
        return self.check_element_is_inactive("Тестовый статус 1", self.TEST_STATUS_1_PARENT)

    # ========== МЕТОДЫ-ОБЕРТКИ ДЛЯ РАЗРЕШЕНИЙ ДИАЛОГОВ ==========

    @allure.step("Нажатие на переключатель 'Сохранить доступ к диалогам'")
    def click_toggle_save_dialog_access(self):
        """Нажимает на переключатель сохранения доступа к диалогам."""
        return self.click_toggle_element("Сохранить доступ к диалогам", self.SAVE_DIALOG_ACCESS)

    @allure.step("Проверка и активация 'Сохранить доступ к диалогам' если он не активен")
    def check_and_activate_save_dialog_access(self):
        """Проверяет и активирует сохранение доступа к диалогам при необходимости."""
        return self.check_and_activate_element(
            "Сохранить доступ к диалогам", 
            self.SAVE_DIALOG_ACCESS, 
            self.SAVE_DIALOG_ACCESS_PARENT
        )

    @allure.step("Проверка и деактивация 'Сохранить доступ к диалогам' если он активирован")
    def check_and_deactivate_save_dialog_access(self):
        """Проверяет и деактивирует сохранение доступа к диалогам при необходимости."""
        return self.check_and_deactivate_element(
            "Сохранить доступ к диалогам", 
            self.SAVE_DIALOG_ACCESS, 
            self.SAVE_DIALOG_ACCESS_PARENT
        )

    @allure.step("Проверка что 'Сохранить доступ к диалогам' активировано")
    def check_activate_save_dialog_access(self):
        """Проверяет что сохранение доступа к диалогам активировано."""
        return self.check_element_is_active("Сохранить доступ к диалогам", self.SAVE_DIALOG_ACCESS_PARENT)

    @allure.step("Проверка что 'Сохранить доступ к диалогам' деактивировано")
    def check_deactivate_save_dialog_access(self):
        """Проверяет что сохранение доступа к диалогам деактивировано."""
        return self.check_element_is_inactive("Сохранить доступ к диалогам", self.SAVE_DIALOG_ACCESS_PARENT)

    # Методы для редактирования информации о диалогах
    @allure.step("Нажатие на переключатель 'Редактировать информацию о диалогах'")
    def click_toggle_edit_dialog_info(self):
        """Нажимает на переключатель редактирования информации о диалогах."""
        return self.click_toggle_element("Редактировать информацию о диалогах", self.EDIT_DIALOG_INFO)

    @allure.step("Проверка и активация 'Редактировать информацию о диалогах' если он не активен")
    def check_and_activate_edit_dialog_info(self):
        """Проверяет и активирует редактирование информации о диалогах при необходимости."""
        return self.check_and_activate_element(
            "Редактировать информацию о диалогах", 
            self.EDIT_DIALOG_INFO, 
            self.EDIT_DIALOG_INFO_PARENT
        )

    @allure.step("Проверка и деактивация 'Редактировать информацию о диалогах' если он активирован")
    def check_and_deactivate_edit_dialog_info(self):
        """Проверяет и деактивирует редактирование информации о диалогах при необходимости."""
        return self.check_and_deactivate_element(
            "Редактировать информацию о диалогах", 
            self.EDIT_DIALOG_INFO, 
            self.EDIT_DIALOG_INFO_PARENT
        )

    @allure.step("Проверка что 'Редактировать информацию о диалогах' активировано")
    def check_activate_edit_dialog_info(self):
        """Проверяет что редактирование информации о диалогах активировано."""
        return self.check_element_is_active("Редактировать информацию о диалогах", self.EDIT_DIALOG_INFO_PARENT)

    @allure.step("Проверка что 'Редактировать информацию о диалогах' деактивировано")
    def check_deactivate_edit_dialog_info(self):
        """Проверяет что редактирование информации о диалогах деактивировано."""
        return self.check_element_is_inactive("Редактировать информацию о диалогах", self.EDIT_DIALOG_INFO_PARENT)

    # Методы для просмотра контактной информации
    @allure.step("Нажатие на переключатель 'Просмотр контактной информации'")
    def click_toggle_view_contact_info(self):
        """Нажимает на переключатель просмотра контактной информации."""
        return self.click_toggle_element("Просмотр контактной информации", self.VIEW_CONTACT_INFO)

    @allure.step("Проверка и активация 'Просмотр контактной информации' если он не активен")
    def check_and_activate_view_contact_info(self):
        """Проверяет и активирует просмотр контактной информации при необходимости."""
        return self.check_and_activate_element(
            "Просмотр контактной информации", 
            self.VIEW_CONTACT_INFO, 
            self.VIEW_CONTACT_INFO_PARENT
        )

    @allure.step("Проверка и деактивация 'Просмотр контактной информации' если он активирован")
    def check_and_deactivate_view_contact_info(self):
        """Проверяет и деактивирует просмотр контактной информации при необходимости."""
        return self.check_and_deactivate_element(
            "Просмотр контактной информации", 
            self.VIEW_CONTACT_INFO, 
            self.VIEW_CONTACT_INFO_PARENT
        )
    @allure.step("Проверка что 'Просмотр контактной информации' активировано")
    def check_activate_view_contact_info(self):
        """Проверяет что просмотр контактной информации активирован."""
        return self.check_element_is_active("Просмотр контактной информации", self.VIEW_CONTACT_INFO_PARENT)

    @allure.step("Проверка что 'Просмотр контактной информации' деактивировано")
    def check_deactivate_view_contact_info(self):
        """Проверяет что просмотр контактной информации деактивирован."""
        return self.check_element_is_inactive("Просмотр контактной информации", self.VIEW_CONTACT_INFO_PARENT)

    # Методы для выгрузки контактов
    @allure.step("Нажатие на переключатель 'Выгружать контакты'")
    def click_toggle_export_contacts(self):
        """Нажимает на переключатель выгрузки контактов."""
        return self.click_toggle_element("Выгружать контакты", self.EXPORT_CONTACTS)

    @allure.step("Проверка и активация 'Выгружать контакты'")
    def check_and_activate_export_contacts(self):
        """Проверяет и активирует выгрузку контактов при необходимости."""
        return self.check_and_activate_element(
            "Выгружать контакты", 
            self.EXPORT_CONTACTS, 
            self.EXPORT_CONTACTS_PARENT
        )

    @allure.step("Проверка и деактивация 'Выгружать контакты'")
    def check_and_deactivate_export_contacts(self):
        """Проверяет и деактивирует выгрузку контактов при необходимости."""
        return self.check_and_deactivate_element(
            "Выгружать контакты", 
            self.EXPORT_CONTACTS, 
            self.EXPORT_CONTACTS_PARENT
        )
    @allure.step("Проверка что 'Выгружать контакты' активировано")
    def check_activate_export_contacts(self):
        """Проверяет что выгрузка контактов активирована."""
        return self.check_element_is_active("Выгружать контакты", self.EXPORT_CONTACTS_PARENT)

    @allure.step("Проверка что 'Выгружать контакты' деактивировано")
    def check_deactivate_export_contacts(self):
        """Проверяет что выгрузка контактов деактивирована."""
        return self.check_element_is_inactive("Выгружать контакты", self.EXPORT_CONTACTS_PARENT)
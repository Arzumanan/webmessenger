"""
Тесты для страницы контактов
"""
from time import sleep
import pytest
import allure
from pages.base_test import BaseTest
from config.data import admin2_email, admin2_password


class TestContacts(BaseTest):
    """Класс тестов для работы с контактами"""
    
    @pytest.mark.skip(reason="Создание контакта - найден баг https://atlassian.i2crm.ru/jira/browse/SCRUMDEV-3910")
    @allure.title("Создание контакта")
    def test_create_contact(self):
        """Тест создания нового контакта"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Данные для создания контакта
        contact_data = {
            'channel': 'telegram',
            'name': 'Тестовый Контакт1',
            'login': '+79963965523',
            'phone': '+79963965523',
            'message': 'Тестовое сообщение для контакта1'
        }
        
        with allure.step("Создание контакта с полными данными"):
            # Создание контакта
            self.contacts_page.create_contact(
                channel=contact_data['channel'],
                name=contact_data['name'],
                login=contact_data['login'],
                phone=contact_data['phone'],
                message=contact_data['message']
            )
            sleep(2)
            # Проверка успешного создания
            assert self.contacts_page.is_success_message_displayed(), \
                "Сообщение об успешном создании контакта не отображается"
            
            success_message = self.contacts_page.get_success_message_text()
            assert "создан" in success_message.lower() or "добавлен" in success_message.lower(), \
                f"Неожиданное сообщение об успехе: {success_message}"
            
            # Проверка, что контакт появился в списке
            assert self.contacts_page.is_contact_exists(contact_data['name']), \
                f"Контакт '{contact_data['name']}' не найден в списке"
            
            # Проверка информации о контакте
            contact_info = self.contacts_page.get_contact_info(contact_data['name'])
            assert contact_info is not None, "Информация о контакте не получена"
            assert contact_info['name'] == contact_data['name'], "Имя контакта не совпадает"
            
            print(f"✅ Контакт '{contact_data['name']}' успешно создан")
    
    @allure.title("Поиск контакта")
    def test_search_contact(self):
        """Тест поиска контакта"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Создаем тестовый контакт для поиска
        test_contact = {
            'channel': 'whatsapp',
            'name': 'Поисковый Контакт',
            'login': '@searchcontact',
            'phone': '+79007654321',
            'message': 'Контакт для тестирования поиска'
        }
        
        # self.contacts_page.create_contact(**test_contact)
        
        # with allure.step("Поиск контакта по имени"):
        #     # Поиск по имени
        #     self.contacts_page.search_contact(test_contact['name'])
            
        #     # Проверка, что найденный контакт отображается
        #     assert self.contacts_page.is_contact_exists(test_contact['name']), \
        #         f"Контакт '{test_contact['name']}' не найден при поиске по имени"
            
        #     print(f"✅ Поиск по имени '{test_contact['name']}' работает корректно")
        with allure.step("Поиск контакта по имени"):
        #     # Поиск по имени
             self.contacts_page.search_contact('МТС 0826')

            # Проверка, что найденный контакт отображается
        assert self.contacts_page.is_contact_exists('МТС 0826'), \
                f"Контакт 'МТС 0826' не найден при поиске по имени"
            
        print(f"✅ Поиск по имени 'МТС 0826' работает корректно")
        sleep(3)

        with allure.step("Поиск контакта по логину"):
            # Поиск по логину
            self.contacts_page.search_contact('vetaw')
            
            # Проверка, что найденный контакт отображается
            assert self.contacts_page.is_contact_exists('Майя Соболевская (Роккосовская)'), \
                f"Контакт не найден при поиске по логину 'vetaw'"
            
            print(f"✅ Поиск по логину 'vetaw' работает корректно")
        
        with allure.step("Поиск контакта по телефону"):
            # Поиск по телефону
            self.contacts_page.search_contact('9963965523')
            
            # Проверка, что найденный контакт отображается
            assert self.contacts_page.is_contact_exists('Мой Номер Йота'), \
                f"Контакт не найден при поиске по телефону '9963965523'"
            
            print(f"✅ Поиск по телефону '9963965523' работает корректно")
    
    # @pytest.mark.skip(reason="Фильтрация тесты еще не написаны")
    @allure.title("Фильтрация контактов по каналу")
    def test_filter_contacts_by_channel(self):
        """Тест фильтрации контактов по каналу"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Создаем контакты для разных каналов
        # contacts_data = [
        #     {'channel': 'telegram', 'name': 'Telegram Контакт', 'login': '@tgcontact', 'phone': '+79001111111'},
        #     {'channel': 'whatsapp', 'name': 'WhatsApp Контакт', 'login': '@wacontact', 'phone': '+79002222222'},
        #     {'channel': 'viber', 'name': 'Viber Контакт', 'login': '@vibercontact', 'phone': '+79003333333'}
        # ]
        
        # for contact in contacts_data:
        #     self.contacts_page.create_contact(**contact)


        # with allure.step("Фильтрация по каналу все"):
        #     # Фильтрация по всем каналам
        #     self.contacts_page.filter_by_channel('all')
            
        #     # Проверка, что отображаются все контакты
        #     assert self.contacts_page.is_contact_exists('Все контакты'), "Все контакты не найдены после фильтрации"
            
        #     print("✅ Фильтрация по каналу все работает корректно")

        
        with allure.step("Фильтрация по каналу instagram"):
            # Фильтрация по instagram
            self.contacts_page.filter_by_channel('instagram')

            assert self.contacts_page.is_contact_exists('Катя Лескина Катерина Кэйт Кот куда идет'), \
                f"Контакт не найден при поиске по телефону 'Катя Лескина Катерина Кэйт Кот куда идет'"
            
            print(f"✅ Поиск по телефону 'Катя Лескина Катерина Кэйт Кот куда идет' работает корректно")
            
        with allure.step("Фильтрация по каналу telegram"):
            # Фильтрация по instagram
            self.contacts_page.filter_by_channel('telegram')

            assert self.contacts_page.is_contact_exists('Я'), \
                    f"Контакт не найден при поиске по телефону 'Я'"
            
            print(f"✅ Поиск по телефону 'Я' работает корректно")
            




            # Проверка, что отображаются только instagram контакты
            # instagram_contact = self.contacts_page.find_contact_by_name('Катя Лескина Катерина Кэйт Кот куда идет')
            # assert instagram_contact is not None, "instagram контакт не найден после фильтрации"
            
            # print("✅ Фильтрация по каналу instagram работает корректно")
        
        # with allure.step("Фильтрация по каналу WhatsApp"):
        #     # Фильтрация по WhatsApp
        #     self.contacts_page.filter_by_channel('whatsapp')
            
        #     # Проверка, что отображаются только WhatsApp контакты
        #     whatsapp_contact = self.contacts_page.find_contact_by_name('WhatsApp Контакт')
        #     assert whatsapp_contact is not None, "WhatsApp контакт не найден после фильтрации"
            
        #     print("✅ Фильтрация по каналу WhatsApp работает корректно")
        
        # with allure.step("Очистка фильтров"):
        #     # Очистка фильтров
        #     self.contacts_page.clear_filters()
            
        #     # Проверка, что все контакты отображаются
        #     for contact in contacts_data:
        #         assert self.contacts_page.is_contact_exists(contact['name']), \
        #             f"Контакт '{contact['name']}' не найден после очистки фильтров"
            
        #     print("✅ Очистка фильтров работает корректно")
    
    @pytest.mark.skip(reason="Выгрузка файла с контактами - тесты еще не написаны")
    @allure.title("Выгрузка файла с контактами")
    def test_export_contacts(self):
        """Тест выгрузки контактов в файл"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Создаем тестовые контакты для выгрузки
        # test_contacts = [
        #     {'channel': 'telegram', 'name': 'Экспорт Контакт 1', 'login': '@export1', 'phone': '+79004444444'},
        #     {'channel': 'whatsapp', 'name': 'Экспорт Контакт 2', 'login': '@export2', 'phone': '+79005555555'}
        # ]
        
        # for contact in test_contacts:
        #     self.contacts_page.create_contact(**contact)
        
        with allure.step("Выгрузка контактов в Excel"):
            # Выгрузка в Excel
            self.contacts_page.export_contacts_excel()
            
            # Проверка успешной выгрузки
            assert self.contacts_page.is_success_message_displayed(), \
                "Сообщение об успешной выгрузке Excel не отображается"
            
            success_message = self.contacts_page.get_success_message_text()
            assert "выгружен" in success_message.lower() or "экспорт" in success_message.lower(), \
                f"Неожиданное сообщение об успехе: {success_message}"
            
            print("✅ Выгрузка в Excel работает корректно")
        
        with allure.step("Выгрузка контактов в CSV"):
            # Выгрузка в CSV
            self.contacts_page.export_contacts_csv()
            
            # Проверка успешной выгрузки
            assert self.contacts_page.is_success_message_displayed(), \
                "Сообщение об успешной выгрузке CSV не отображается"
            
            success_message = self.contacts_page.get_success_message_text()
            assert "выгружен" in success_message.lower() or "экспорт" in success_message.lower(), \
                f"Неожиданное сообщение об успехе: {success_message}"
            
            print("✅ Выгрузка в CSV работает корректно")
    
    @pytest.mark.skip(reason="Редактирование контакта - тесты еще не написаны")
    @allure.title("Редактирование контакта")
    def test_edit_contact(self):
        """Тест редактирования контакта"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Создаем контакт для редактирования
        original_contact = {
            'channel': 'telegram',
            'name': 'Редактируемый Контакт',
            'login': '@original',
            'phone': '+79006666666'
        }
        
        self.contacts_page.create_contact(**original_contact)
        
        with allure.step("Редактирование данных контакта"):
            # Редактирование контакта
            new_data = {
                'new_channel': 'whatsapp',
                'new_name': 'Обновленный Контакт',
                'new_login': '@updated',
                'new_phone': '+79007777777'
            }
            
            self.contacts_page.edit_contact(
                contact_name=original_contact['name'],
                new_channel=new_data['new_channel'],
                new_name=new_data['new_name'],
                new_login=new_data['new_login'],
                new_phone=new_data['new_phone']
            )
            
            # Проверка успешного редактирования
            assert self.contacts_page.is_success_message_displayed(), \
                "Сообщение об успешном редактировании не отображается"
            
            # Проверка, что старый контакт не существует
            assert not self.contacts_page.is_contact_exists(original_contact['name']), \
                "Старый контакт все еще существует"
            
            # Проверка, что новый контакт существует
            assert self.contacts_page.is_contact_exists(new_data['new_name']), \
                "Обновленный контакт не найден"
            
            # Проверка данных обновленного контакта
            updated_contact_info = self.contacts_page.get_contact_info(new_data['new_name'])
            assert updated_contact_info is not None, "Информация об обновленном контакте не получена"
            
            print(f"✅ Контакт успешно отредактирован: {new_data['new_name']}")
    
    @pytest.mark.skip(reason="Удаление контакта - тесты еще не написаны")
    @allure.title("Удаление контакта")
    def test_delete_contact(self):
        """Тест удаления контакта"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Создаем контакт для удаления
        contact_to_delete = {
            'channel': 'viber',
            'name': 'Удаляемый Контакт',
            'login': '@todelete',
            'phone': '+79008888888'
        }
        
        self.contacts_page.create_contact(**contact_to_delete)
        
        # Проверяем, что контакт создан
        assert self.contacts_page.is_contact_exists(contact_to_delete['name']), \
            "Контакт для удаления не найден"
        
        with allure.step("Удаление контакта"):
            # Удаление контакта
            self.contacts_page.delete_contact(contact_to_delete['name'])
            
            # Проверка успешного удаления
            assert self.contacts_page.is_success_message_displayed(), \
                "Сообщение об успешном удалении не отображается"
            
            success_message = self.contacts_page.get_success_message_text()
            assert "удален" in success_message.lower() or "удален" in success_message.lower(), \
                f"Неожиданное сообщение об успехе: {success_message}"
            
            # Проверка, что контакт больше не существует
            assert not self.contacts_page.is_contact_exists(contact_to_delete['name']), \
                "Контакт все еще существует после удаления"
            
            print(f"✅ Контакт '{contact_to_delete['name']}' успешно удален")
    
    @pytest.mark.skip(reason="Архивация контакта - тесты еще не написаны")
    @allure.title("Архивация контакта")
    def test_archive_contact(self):
        """Тест архивации контакта"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Создаем контакт для архивации
        contact_to_archive = {
            'channel': 'sms',
            'name': 'Архивный Контакт',
            'login': '@toarchive',
            'phone': '+79009999999'
        }
        
        self.contacts_page.create_contact(**contact_to_archive)
        
        # Проверяем, что контакт создан
        assert self.contacts_page.is_contact_exists(contact_to_archive['name']), \
            "Контакт для архивации не найден"
        
        with allure.step("Архивация контакта"):
            # Архивация контакта
            self.contacts_page.archive_contact(contact_to_archive['name'])
            
            # Проверка успешной архивации
            assert self.contacts_page.is_success_message_displayed(), \
                "Сообщение об успешной архивации не отображается"
            
            success_message = self.contacts_page.get_success_message_text()
            assert "архивирован" in success_message.lower() or "архив" in success_message.lower(), \
                f"Неожиданное сообщение об успехе: {success_message}"
            
            # Проверка, что контакт заархивирован (не отображается в основном списке)
            assert not self.contacts_page.is_contact_exists(contact_to_archive['name']), \
                "Заархивированный контакт все еще отображается в основном списке"
            
            print(f"✅ Контакт '{contact_to_archive['name']}' успешно заархивирован")
    
    @pytest.mark.skip(reason="Отправка сообщения контакту - тесты еще не написаны")
    @allure.title("Отправка сообщения контакту")
    def test_send_message_to_contact(self):
        """Тест отправки сообщения контакту"""
        # Логин как админ
        self.contacts_page.open_host()
        self.login_admin_page.open_admin_login_page()
        self.login_admin_page.enter_email(admin2_email)
        self.login_admin_page.enter_password(admin2_password)
        self.login_admin_page.admin_authorization()
        
        # Переход на страницу контактов
        self.contacts_page.open_contacts_page()
        
        # Создаем контакт для отправки сообщения
        contact_for_message = {
            'channel': 'telegram',
            'name': 'Контакт для Сообщения',
            'login': '@formessage',
            'phone': '+79001010101'
        }
        
        self.contacts_page.create_contact(**contact_for_message)
        
        with allure.step("Отправка сообщения контакту"):
            # Отправка сообщения
            test_message = "Тестовое сообщение для контакта"
            self.contacts_page.send_message_to_contact(contact_for_message['name'], test_message)
            
            # Проверка успешной отправки
            assert self.contacts_page.is_success_message_displayed(), \
                "Сообщение об успешной отправке не отображается"
            
            success_message = self.contacts_page.get_success_message_text()
            assert "отправлено" in success_message.lower() or "отправлено" in success_message.lower(), \
                f"Неожиданное сообщение об успехе: {success_message}"
            
            print(f"✅ Сообщение успешно отправлено контакту '{contact_for_message['name']}'")

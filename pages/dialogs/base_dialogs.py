import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from pages.login_admin_page import LoginAdminPage
from config.data import admin_ura_email, admin_ura_password


class BaseDialogsPage(BasePage):
    """Базовый класс для работы с диалогами"""
    
    # Локаторы для диалогов
    DIALOGS_NAV_LINK = ("xpath", "//a[@id='dialogs' and @href='/dialogs']")
    ACTIVE_DIALOGS_NAV = ("xpath", "//a[@class='navlink active' and @id='dialogs']")
    SIDEBAR_HEADER_TEXT = ("xpath", "//span[@class='sidebar-header-profile-name']")
    DIALOGS_CONTENT = ("xpath", "//*[contains(@class, 'dialog') or contains(@class, 'message') or contains(@class, 'chat')]")
    
    # Локаторы для поиска
    SEARCH_INPUT = ("xpath", "//input[@class='sidebar-header-search-field-input' and @type='text' and @placeholder='Поиск']")
    SEARCH_INPUT_ALT = ("xpath", "//input[contains(@class, 'search-field-input') and @type='text']")
    SEARCH_RESULTS = ("xpath", "//*[contains(@class, 'search-result') or contains(@class, 'dialog')]")
    DIALOG_ITEMS = ("xpath", "//div[contains(@class, 'last-message')]")
    DIALOG_NAMES = ("xpath", "//p[contains(@class, 'last-message__name')]")
    
    # Локаторы для диалога
    DIALOG_ITEM = ("xpath", "//div[@class='last-message']//p[@class='last-message__name' and contains(text(), 'Юрий Арзуманян  - Telegram - ura_testt2')]/..")
    DIALOG_ITEM_ALT = ("xpath", "//div[contains(@class, 'last-message')]//p[contains(@class, 'last-message__name') and contains(text(), 'Юрий Арзуманян') and contains(text(), 'ura_testt2')]/..")
    
    # Локаторы для отправки сообщений
    MESSAGE_TEXTAREA = ("xpath", "//textarea[@class='mainbar-chat-area' and @placeholder='Напишите сообщение...']")
    MESSAGE_TEXTAREA_ALT = ("xpath", "//textarea[contains(@class, 'mainbar-chat-area')]")
    SEND_BUTTON = ("xpath", "//button[contains(@class, 'send-button') or contains(@class, 'send')]")
    
    # Локаторы для фильтра диалогов
    FILTER_TOGGLE_BUTTON = ("xpath", "//button[contains(@class, 'dialogs-filter__toggle-filter-btn')]")
    EXPIRED_DIALOGS_TOGGLE = ("xpath", "//div[@class='toggle-with-text']//p[text()='Показать просроченные диалоги']/preceding-sibling::label//input[@type='checkbox']")
    EXPIRED_DIALOGS_TOGGLE_CONTAINER = ("xpath", "//div[@class='toggle-with-text']//p[text()='Показать просроченные диалоги']/preceding-sibling::label")
    EXPIRED_DIALOGS_TEXT = ("xpath", "//p[@class='toggle-with-text__text' and text()='Показать просроченные диалоги']")
    
    @allure.step("Авторизация admin_ura")
    def login_as_admin_ura(self):
        """Полная авторизация пользователя admin_ura"""
        login_page = LoginAdminPage(self.browser)
        
        # Открываем главную страницу
        self.open_host()
        assert "Веб-мессенджер" in self.browser.title, "Не удалось открыть главную страницу"
        
        # Переходим на страницу авторизации
        login_page.open_admin_login_page()
        
        # Вводим данные для авторизации
        login_page.enter_email(admin_ura_email)
        login_page.enter_password(admin_ura_password)
        
        # Выполняем авторизацию
        login_page.admin_authorization()
        
        # Ожидаем успешной авторизации и автоматического перехода в диалоги
        WebDriverWait(self.browser, 20).until(
            lambda d: "/login" not in d.current_url and "/dialogs" in d.current_url,
            "Авторизация не завершилась или не произошел переход в диалоги"
        )
        
        return self

    @allure.step("Авторизация менеджера")
    def login_as_manager(self):
        """Полная авторизация пользователя admin_ura"""
        from pages.login_admin_page import LoginAdminPage
        from config.data import admin_ura_email, admin_ura_password
        
        login_page = LoginAdminPage(self.browser)
        
        # Открываем главную страницу
        self.open_host()
        assert "Веб-мессенджер" in self.browser.title, "Не удалось открыть главную страницу"
        
        # Переходим на страницу авторизации
        login_page.open_admin_login_page()
        
        # Вводим данные для авторизации
        login_page.enter_email(admin_ura_email)
        login_page.enter_password(admin_ura_password)
        
        # Выполняем авторизацию
        login_page.admin_authorization()
        
        # Ожидаем успешной авторизации и перехода в диалоги
        WebDriverWait(self.browser, 20).until(
            lambda d: "/login" not in d.current_url and "/dialogs" in d.current_url,
            "Авторизация admin_ura не завершилась или не произошел переход в диалоги"
        )
        
        return self

    @allure.step("Переход в диалоги")
    def navigate_to_dialogs(self):
        """Переход в раздел диалогов"""
        # Кликаем по ссылке диалогов
        dialogs_link = self.element_in_clickable(self.DIALOGS_NAV_LINK)
        dialogs_link.click()
        
        # Ожидаем загрузки страницы диалогов
        WebDriverWait(self.browser, 10).until(
            lambda d: "/dialogs" in d.current_url,
            "Не произошел переход в диалоги"
        )
        
        return self

    @allure.step("Нажатие на кнопку фильтра")
    def click_filter_toggle_button(self):
        """Нажатие на кнопку переключения фильтра диалогов"""
        try:
            # Ждем появления кнопки фильтра
            filter_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(self.FILTER_TOGGLE_BUTTON),
                "Кнопка фильтра не найдена"
            )
            
            # Прокручиваем к кнопке, если необходимо
            self.browser.execute_script("arguments[0].scrollIntoView(true);", filter_button)
            
            # Небольшая пауза перед кликом
            self.browser.implicitly_wait(1)
            
            # Пробуем кликнуть по кнопке разными способами
            try:
                filter_button.click()
            except:
                # Если обычный клик не работает, используем JavaScript
                self.browser.execute_script("arguments[0].click();", filter_button)
            
            # Ждем, чтобы фильтр открылся и появилась надпись
            WebDriverWait(self.browser, 5).until(
                EC.presence_of_element_located(self.EXPIRED_DIALOGS_TEXT),
                "Надпись 'Показать просроченные диалоги' не появилась"
            )
            
            allure.attach(
                "Нажата кнопка фильтра диалогов, появилась панель фильтров",
                name="Кнопка фильтра",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return self
            
        except Exception as e:
            allure.attach(
                f"Ошибка при нажатии на кнопку фильтра: {str(e)}",
                name="Ошибка кнопки фильтра",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.step("Включение переключателя показа истекших диалогов")
    def toggle_expired_dialogs_filter(self):
        """Включение переключателя показа истекших диалогов"""
        try:
            # Пробуем найти переключатель по основному локатору
            toggle_container = None
            try:
                toggle_container = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable(self.EXPIRED_DIALOGS_TOGGLE_CONTAINER),
                    "Основной переключатель истекших диалогов не найден"
                )
            except:
                # Если основной локатор не сработал, пробуем альтернативный
                alternative_locator = ("xpath", "//div[contains(@class, 'toggle-with-text')]//p[contains(text(), 'Показать просроченные диалоги')]/preceding-sibling::label")
                toggle_container = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable(alternative_locator),
                    "Альтернативный переключатель истекших диалогов не найден"
                )
            
            # Прокручиваем к переключателю, если необходимо
            self.browser.execute_script("arguments[0].scrollIntoView(true);", toggle_container)
            
            # Небольшая пауза перед кликом
            self.browser.implicitly_wait(1)
            
            # Кликаем по контейнеру переключателя
            toggle_container.click()
            
            # Ждем, чтобы переключатель сработал
            self.browser.implicitly_wait(2)
            
            allure.attach(
                "Включен переключатель показа истекших диалогов",
                name="Переключатель истекших диалогов",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return self
            
        except Exception as e:
            allure.attach(
                f"Ошибка при включении переключателя истекших диалогов: {str(e)}",
                name="Ошибка переключателя",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.step("Проверка включения переключателя истекших диалогов")
    def verify_expired_dialogs_toggle_enabled(self):
        """Проверка, что переключатель показа истекших диалогов включен"""
        try:
            # Пробуем найти переключатель по основному локатору
            toggle_input = None
            try:
                toggle_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(self.EXPIRED_DIALOGS_TOGGLE),
                    "Основной переключатель истекших диалогов не найден"
                )
            except:
                # Если основной локатор не сработал, пробуем альтернативный
                alternative_locator = ("xpath", "//div[contains(@class, 'toggle-with-text')]//p[contains(text(), 'Показать просроченные диалоги')]/preceding-sibling::label//input[@type='checkbox']")
                toggle_input = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located(alternative_locator),
                    "Альтернативный переключатель истекших диалогов не найден"
                )
            
            # Проверяем, что переключатель включен
            is_checked = toggle_input.is_selected()
            
            allure.attach(
                f"Состояние переключателя истекших диалогов: {'включен' if is_checked else 'выключен'}",
                name="Состояние переключателя",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return is_checked
            
        except Exception as e:
            allure.attach(
                f"Ошибка при проверке состояния переключателя: {str(e)}",
                name="Ошибка проверки",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    @allure.step("Проверка появления надписи 'Показать просроченные диалоги'")
    def verify_expired_dialogs_text_appeared(self):
        """Проверка появления надписи 'Показать просроченные диалоги'"""
        try:
            # Ждем появления надписи
            expired_dialogs_text = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(self.EXPIRED_DIALOGS_TEXT),
                "Надпись 'Показать просроченные диалоги' не появилась"
            )
            
            is_visible = expired_dialogs_text.is_displayed()
            
            allure.attach(
                f"Надпись 'Показать просроченные диалоги': {'видна' if is_visible else 'не видна'}",
                name="Надпись фильтра",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return is_visible
            
        except Exception as e:
            allure.attach(
                f"Ошибка при проверке надписи: {str(e)}",
                name="Ошибка проверки надписи",
                attachment_type=allure.attachment_type.TEXT
            )
            return False

    @allure.step("Проверка перехода в диалоги")
    def verify_dialogs_navigation(self):
        """Проверка успешного перехода в раздел диалогов"""
        # Проверяем URL
        current_url = self.browser.current_url
        assert "/dialogs" in current_url, f"Текущий URL {current_url} не содержит /dialogs"
        
        # Проверяем активное состояние навигации
        active_nav = self.element_in_visible(self.ACTIVE_DIALOGS_NAV)
        assert active_nav.is_displayed(), "Элемент навигации диалогов не отображается"
        
        # Проверяем текст в sidebar
        sidebar_text = self.element_in_visible(self.SIDEBAR_HEADER_TEXT)
        assert sidebar_text.text == "Диалоги", f"Ожидался текст 'Диалоги', получен '{sidebar_text.text}'"
        
        return self

    @allure.step("Проверка интерфейса диалогов")
    def verify_dialogs_interface(self):
        """Проверка наличия элементов интерфейса диалогов"""
        try:
            dialogs_elements = self.browser.find_elements(*self.DIALOGS_CONTENT)
            allure.attach(
                f"Найдено элементов диалогов: {len(dialogs_elements)}",
                name="Диалоги интерфейс",
                attachment_type=allure.attachment_type.TEXT
            )
            return len(dialogs_elements)
        except Exception as e:
            allure.attach(
                f"Не удалось найти элементы интерфейса диалогов: {str(e)}",
                name="Диалоги интерфейс",
                attachment_type=allure.attachment_type.TEXT
            )
            return 0

    @allure.step("Полная проверка диалогов")
    def verify_dialogs_page(self):
        """Комплексная проверка страницы диалогов"""
        self.verify_dialogs_navigation()
        elements_count = self.verify_dialogs_interface()
        return elements_count

    @allure.step("Поиск в диалогах")
    def search_in_dialogs(self, search_text):
        """Поиск диалогов по тексту"""
        search_input = None
        
        try:
            # Пробуем найти поле поиска по основному локатору
            try:
                search_input = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable(self.SEARCH_INPUT),
                    "Основное поле поиска не найдено"
                )
            except:
                # Если основной локатор не сработал, пробуем альтернативный
                search_input = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable(self.SEARCH_INPUT_ALT),
                    "Альтернативное поле поиска не найдено"
                )
            
            # Очищаем поле и вводим текст поиска
            search_input.clear()
            search_input.send_keys(search_text)
            
            # Ждем, чтобы поиск обработался и DOM обновился
            self.browser.implicitly_wait(3)
            
            # Дополнительная пауза для стабилизации результатов
            import time
            time.sleep(1)
            
            allure.attach(
                f"Выполнен поиск по тексту: '{search_text}'",
                name="Поиск выполнен",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return self
            
        except Exception as e:
            allure.attach(
                f"Ошибка при поиске: {str(e)}",
                name="Ошибка поиска",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.step("Проверка результатов поиска")
    def verify_search_results(self, expected_text):
        """Проверка результатов поиска"""
        try:
            # Ждем немного, чтобы результаты поиска загрузились
            self.browser.implicitly_wait(2)
            
            # Ищем диалоги
            dialog_items = self.browser.find_elements(*self.DIALOG_ITEMS)
            dialog_names = self.browser.find_elements(*self.DIALOG_NAMES)
            
            # Логируем найденные элементы для отладки
            allure.attach(
                f"Найдено диалогов: {len(dialog_items)}, имен диалогов: {len(dialog_names)}",
                name="Количество элементов",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Проверяем, что есть диалоги
            assert len(dialog_items) > 0 or len(dialog_names) > 0, f"Не найдено диалогов для поиска '{expected_text}'"
            
            # Проверяем, что в результатах есть искомый текст
            found_text = False
            found_elements = []
            
            # Проверяем в именах диалогов
            for name_element in dialog_names:
                element_text = name_element.text.strip()
                if element_text:
                    found_elements.append(element_text)
                    if expected_text.lower() in element_text.lower():
                        found_text = True
                        break
            
            # Если не нашли в именах, проверяем в диалогах
            if not found_text:
                for dialog_element in dialog_items:
                    element_text = dialog_element.text.strip()
                    if element_text:
                        found_elements.append(element_text)
                        if expected_text.lower() in element_text.lower():
                            found_text = True
                            break
            
            # Логируем найденные тексты для отладки
            allure.attach(
                f"Найденные тексты: {found_elements[:10]}",  # Показываем первые 10
                name="Найденные тексты",
                attachment_type=allure.attachment_type.TEXT
            )
            
            if not found_text:
                allure.attach(
                    f"Искомый текст: '{expected_text}'",
                    name="Искомый текст",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            assert found_text, f"В результатах поиска не найден текст '{expected_text}'. Найдены: {found_elements[:5]}"
            
            allure.attach(
                f"Найдено результатов поиска: {len(found_elements)}",
                name="Результаты поиска",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return len(found_elements)
            
        except Exception as e:
            allure.attach(
                f"Ошибка при проверке результатов поиска: {str(e)}",
                name="Ошибка поиска",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.step("Клик по диалогу")
    def click_on_dialog(self, dialog_name):
        """Клик по найденному диалогу"""
        dialog_element = None
        
        try:
            # Ждем немного, чтобы результаты поиска загрузились
            self.browser.implicitly_wait(3)
            
            # Пробуем найти диалог по основному локатору
            try:
                dialog_element = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable(self.DIALOG_ITEM),
                    "Основной диалог не найден"
                )
            except:
                # Если основной локатор не сработал, пробуем альтернативный
                dialog_element = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable(self.DIALOG_ITEM_ALT),
                    "Альтернативный диалог не найден"
                )
            
            # Прокручиваем к элементу, если необходимо
            self.browser.execute_script("arguments[0].scrollIntoView(true);", dialog_element)
            
            # Небольшая пауза перед кликом
            self.browser.implicitly_wait(1)
            
            # Кликаем по диалогу
            dialog_element.click()
            
            # Небольшая пауза для загрузки диалога
            self.browser.implicitly_wait(2)
            
            allure.attach(
                f"Выполнен клик по диалогу: '{dialog_name}'",
                name="Клик по диалогу",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return self
            
        except Exception as e:
            allure.attach(
                f"Ошибка при клике по диалогу: {str(e)}",
                name="Ошибка клика",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.step("Отправка сообщения")
    def send_message(self, message_text):
        """Отправка сообщения в диалог"""
        try:
            # Ждем появления поля ввода сообщения
            message_textarea = None
            
            try:
                message_textarea = WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable(self.MESSAGE_TEXTAREA),
                    "Поле ввода сообщения не найдено"
                )
            except:
                # Пробуем альтернативный локатор
                message_textarea = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable(self.MESSAGE_TEXTAREA_ALT),
                    "Альтернативное поле ввода сообщения не найдено"
                )
            
            # Прокручиваем к полю ввода
            self.browser.execute_script("arguments[0].scrollIntoView(true);", message_textarea)
            
            # Очищаем поле и вводим сообщение
            message_textarea.clear()
            message_textarea.send_keys(message_text)
            
            # Небольшая пауза перед отправкой
            self.browser.implicitly_wait(1)
            
            # Отправляем сообщение нажатием Enter
            from selenium.webdriver.common.keys import Keys
            message_textarea.send_keys(Keys.ENTER)
            
            # Ждем отправки сообщения
            self.browser.implicitly_wait(2)
            
            allure.attach(
                f"Отправлено сообщение: '{message_text}'",
                name="Сообщение отправлено",
                attachment_type=allure.attachment_type.TEXT
            )
            
            return self
            
        except Exception as e:
            allure.attach(
                f"Ошибка при отправке сообщения: {str(e)}",
                name="Ошибка отправки",
                attachment_type=allure.attachment_type.TEXT
            )
            raise

    @allure.step("Проверка отправки сообщения")
    def verify_message_sent(self, message_text):
        """Проверка успешной отправки сообщения"""
        try:
            # Ждем немного, чтобы сообщение появилось в чате
            self.browser.implicitly_wait(3)
            
            # Ищем отправленное сообщение в чате
            message_locator = ("xpath", f"//*[contains(text(), '{message_text}')]")
            
            try:
                sent_message = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_element_located(message_locator),
                    f"Сообщение '{message_text}' не найдено в чате"
                )
                
                allure.attach(
                    f"Сообщение '{message_text}' успешно отправлено и отображается в чате",
                    name="Проверка отправки",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                return True
                
            except:
                # Если не нашли точное совпадение, ищем частичное
                partial_locator = ("xpath", f"//*[contains(text(), 'Тестовоео сообщение')]")
                try:
                    sent_message = self.browser.find_element(*partial_locator)
                    allure.attach(
                        f"Найдено частичное совпадение сообщения в чате",
                        name="Проверка отправки",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    return True
                except:
                    allure.attach(
                        f"Сообщение не найдено в чате. Искомый текст: '{message_text}'",
                        name="Ошибка проверки",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    return False
                    
        except Exception as e:
            allure.attach(
                f"Ошибка при проверке отправки сообщения: {str(e)}",
                name="Ошибка проверки",
                attachment_type=allure.attachment_type.TEXT
            )
            return False


# Константы для тестов
SEARCH_VARIANTS = [
    "Юрий Арзуманян  - Telegram - ura_testt2",
    "Юрий Арзуманян",
    "ura_testt2",
    "Telegram - ura_testt2"
]

TEST_MESSAGE = "Тестовоео сообщение  в ТГ канал из ВМ"


# Фикстуры для pytest
@pytest.fixture(scope="function")
def dialogs_page(browser):
    """Фикстура для создания экземпляра BaseDialogsPage"""
    return BaseDialogsPage(browser)


@pytest.fixture(scope="function")
def admin_ura_authorized(dialogs_page):
    """Фикстура для авторизации admin_ura"""
    return dialogs_page.login_as_admin_ura()


@pytest.fixture(scope="function")
def dialogs_page_ready(admin_ura_authorized):
    """Фикстура для готовой страницы диалогов с авторизацией"""
    admin_ura_authorized.verify_dialogs_page()
    return admin_ura_authorized


@pytest.fixture(scope="function")
def found_dialog(dialogs_page_ready):
    """Фикстура для поиска и открытия диалога"""
    dialogs_page = dialogs_page_ready
    
    # Выполняем поиск по разным вариантам
    for search_text in SEARCH_VARIANTS:
        try:
            dialogs_page.search_in_dialogs(search_text)
            results_count = dialogs_page.verify_search_results(search_text)
            
            if results_count > 0:
                # Кликаем по найденному диалогу
                dialogs_page.click_on_dialog(search_text)
                return dialogs_page, search_text
        except Exception as e:
            print(f"Поиск по '{search_text}' не удался: {e}")
            continue
    
    # Если ни один поиск не удался
    pytest.fail(f"Не удалось найти диалог ни по одному из вариантов: {SEARCH_VARIANTS}")


@pytest.fixture(scope="function")
def message_sent(found_dialog):
    """Фикстура для отправки сообщения и проверки"""
    dialogs_page, search_text = found_dialog
    
    # Отправляем сообщение
    dialogs_page.send_message(TEST_MESSAGE)
    
    # Проверяем отправку
    message_sent_result = dialogs_page.verify_message_sent(TEST_MESSAGE)
    
    return dialogs_page, TEST_MESSAGE, message_sent_result


@pytest.fixture(scope="function")
def test_message():
    """Фикстура с тестовым сообщением"""
    return TEST_MESSAGE


@pytest.fixture(scope="function")
def test_data():
    """Фикстура с тестовыми данными"""
    return {
        "search_variants": SEARCH_VARIANTS,
        "test_message": TEST_MESSAGE,
        "expected_dialog_name": "Юрий Арзуманян  - Telegram - ura_testt2"
    }

import allure

from config.links import Links
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class TemplatesPage(BasePage):
    PAGE_URL = Links.TEMPLATES_URL

    @allure.step("Открыть страницу шаблонов")
    def open_templates(self):
        return self.open()

    # Локаторы (возможные, с запасом по устойчивости)
    # Кнопка "Добавить Шаблон +"
    ADD_TEMPLATE_BUTTON = (
        By.XPATH,
        "//button[@type='button' and contains(@class,'btn_primary') and contains(normalize-space(.), 'Добавить Шаблон')]",
    )
    # Заголовок модалки: "Новый шаблон"
    MODAL_TITLE = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//div[contains(@class,'add-contact-header-text') and normalize-space(text())='Новый шаблон']",
    )
    # Поле Название шаблона
    NAME_INPUT = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//input[@id='templateName' and @name='templateName']",
    )
    # Поле Текст шаблона
    TEXTAREA_CONTENT = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//textarea[@id='templateText' and @name='templateText']",
    )
    # Кнопка "Создать шаблон"
    SAVE_BUTTON = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//button[@type='submit' and contains(normalize-space(.), 'Создать шаблон')]",
    )

    # Навигация в раздел "Настройки"
    SETTINGS_LINK = (
        By.XPATH,
        "//a[@id='settings' and contains(@class,'navlink')]",
    )
    SETTINGS_TITLE = (
        By.XPATH,
        "//h2[contains(@class,'sidebar__title') and normalize-space(.)='Настройки']",
    )

    # Подсказка о необходимости заполнения полей
    REQUIRED_FIELDS_HINT = (
        By.XPATH,
        "//span[contains(@class,'add-contact-form-control-label-red') and normalize-space(.)='Выделенные поля обязательны для заполнения.']",
    )

    def _wait(self):
        return WebDriverWait(self.browser, 15)

    def _fill_input(self, locator, value: str):
        el = self._wait().until(EC.element_to_be_clickable(locator))
        self.browser.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            el.click(); time.sleep(0.05)
            el.clear(); time.sleep(0.05)
            el.send_keys(value)
        except Exception:
            self.browser.execute_script("arguments[0].value = arguments[1];", el, value)
            self.browser.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", el)
            self.browser.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles:true}));", el)

    @allure.step("Открыть модалку добавления шаблона")
    def open_add_modal(self):
        btn = self._wait().until(EC.element_to_be_clickable(self.ADD_TEMPLATE_BUTTON))
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self._wait().until(EC.visibility_of_element_located(self.MODAL_TITLE))

    @allure.step("Заполнить поля шаблона")
    def fill_template_form(self, name: str, category: str | None, text: str):
        # Заполняем обязательные поля
        self._fill_input(self.NAME_INPUT, name)
        self._fill_input(self.TEXTAREA_CONTENT, text)

    @allure.step("Сохранить шаблон")
    def save_template(self):
        btn = self._wait().until(EC.element_to_be_clickable(self.SAVE_BUTTON))
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)

    @allure.step("Проверить наличие шаблона в списке")
    def assert_template_in_list(self, name: str):
        self._wait().until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(@class,'template') or contains(@class,'list') or self::li]//*[contains(text(),'{name}')] | //*[contains(text(),'{name}')]"))
        )

    @allure.step("Открыть раздел Настройки и проверить заголовок")
    def open_settings_and_check(self):
        link = self._wait().until(EC.element_to_be_clickable(self.SETTINGS_LINK))
        try:
            link.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", link)
        self._wait().until(EC.visibility_of_element_located(self.SETTINGS_TITLE))

    @allure.step("Ожидать валидацию поля 'Текст шаблона'")
    def assert_text_validation_error(self):
        def any_validation(_):
            # 1) Явное сообщение об ошибке в форме
            try:
                err = self.browser.find_element(By.XPATH,
                    "//form[contains(@class,'add-template-form')]//*[contains(@class,'error') or contains(@class,'error-message') or contains(@class,'invalid')][not(self::input) and not(self::textarea)]")
                if err.is_displayed():
                    return True
            except Exception:
                pass
            # 2) Поле textarea имеет состояние ошибки
            try:
                textarea = self.browser.find_element(*self.TEXTAREA_CONTENT)
                cls = (textarea.get_attribute('class') or '').lower()
                aria = (textarea.get_attribute('aria-invalid') or '').lower()
                if 'error' in cls or 'invalid' in cls or aria in ('true', '1'):
                    return True
            except Exception:
                pass
            # 3) Кнопка сохранения задизейблена
            try:
                save = self.browser.find_element(*self.SAVE_BUTTON)
                disabled = save.get_attribute('disabled')
                if disabled is not None and disabled != 'false':
                    return True
            except Exception:
                pass
            return False

        # Пробуем дождаться валидации до 20 секунд
        WebDriverWait(self.browser, 20).until(any_validation)

    @allure.step("Спровоцировать валидацию поля 'Текст' (blur)")
    def trigger_text_validation(self):
        try:
            textarea = self._wait().until(EC.presence_of_element_located(self.TEXTAREA_CONTENT))
            # Сфокусироваться и убрать фокус
            try:
                textarea.click(); time.sleep(0.05)
            except Exception:
                self.browser.execute_script("arguments[0].click();", textarea)
            # Убрать фокус через TAB
            textarea.send_keys("\t")
        except Exception:
            # как альтернатива — кликнуть по заголовку формы, чтобы снять фокус
            try:
                header = self.browser.find_element(By.XPATH, "//div[contains(@class,'add-contact-header-text')]")
                self.browser.execute_script("arguments[0].scrollIntoView({block:'center'});", header)
                try:
                    header.click()
                except Exception:
                    self.browser.execute_script("arguments[0].click();", header)
            except Exception:
                pass

    @allure.step("Проверить наличие текста о обязательных полях")
    def assert_required_fields_hint(self):
        self._wait().until(EC.visibility_of_element_located(self.REQUIRED_FIELDS_HINT))




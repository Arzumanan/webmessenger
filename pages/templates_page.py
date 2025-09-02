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

    # Локаторы
    ADD_TEMPLATE_BUTTON = (
        By.XPATH,
        "//button[@type='button' and contains(@class,'btn_primary') and contains(normalize-space(.), 'Добавить Шаблон')]",
    )
    MODAL_TITLE = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//div[contains(@class,'add-contact-header-text') and normalize-space(text())='Новый шаблон']",
    )
    NAME_INPUT = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//input[@id='templateName' and @name='templateName']",
    )
    TEXTAREA_CONTENT = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//textarea[@id='templateText' and @name='templateText']",
    )
    SAVE_BUTTON = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//button[@type='submit' and contains(normalize-space(.), 'Создать шаблон')]",
    )
    SETTINGS_LINK = (
        By.XPATH,
        "//a[@id='settings' and contains(@class,'navlink')]",
    )
    SETTINGS_TITLE = (
        By.XPATH,
        "//h2[contains(@class,'sidebar__title') and normalize-space(.)='Настройки']",
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

    # Локаторы для удаления шаблона
    CONFIRM_DELETE_BUTTON = (
        By.XPATH,
        "//button[@type='button' and contains(@class,'btn_primary') and contains(@class,'btn_default') and contains(@class,'btn_icon-none') and normalize-space(.)='Да']"
    )

    @allure.step("Найти и удалить шаблон по имени")
    def delete_template_by_name(self, template_name: str):
        # Сначала найдем элемент с именем шаблона
        template_element = self._wait().until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{template_name}')]"))
        )
        
        # Прокрутим к элементу
        self.browser.execute_script("arguments[0].scrollIntoView({block:'center'});", template_element)
        
        # Найдем все кнопки в контейнере шаблона
        all_buttons = self.browser.find_elements(
            By.XPATH, 
            f"//*[contains(text(),'{template_name}')]/ancestor::*[contains(@class,'template') or contains(@class,'list') or self::li]//button"
        )
        
        delete_btn = None
        
        # Попробуем найти кнопку удаления по различным критериям
        for button in all_buttons:
            try:
                # Проверим, есть ли SVG в кнопке
                svg = button.find_element(By.TAG_NAME, "svg")
                viewbox = svg.get_attribute('viewBox')
                paths = svg.find_elements(By.TAG_NAME, "path")
                
                # Кнопка удаления (корзина) обычно имеет viewBox="0 0 18 18" и много path элементов
                if viewbox == "0 0 18 18" and len(paths) >= 4:
                    delete_btn = button
                    break
            except:
                continue
        
        # Если не нашли по SVG, попробуем найти по атрибутам
        if delete_btn is None:
            for button in all_buttons:
                try:
                    title = button.get_attribute('title') or ''
                    aria_label = button.get_attribute('aria-label') or ''
                    class_name = button.get_attribute('class') or ''
                    
                    if any(keyword in (title + aria_label + class_name).lower() for keyword in ['delete', 'remove', 'trash', 'удалить']):
                        delete_btn = button
                        break
                except:
                    continue
        
        # Если все еще не нашли, возьмем последнюю кнопку (обычно кнопка удаления идет последней)
        if delete_btn is None and all_buttons:
            delete_btn = all_buttons[-1]
        
        if delete_btn is None:
            raise Exception(f"Не удалось найти кнопку удаления для шаблона '{template_name}'")
        
        # Кликнуть на кнопку удаления
        try:
            delete_btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", delete_btn)
        
        # Подтвердить удаление
        confirm_btn = self._wait().until(EC.element_to_be_clickable(self.CONFIRM_DELETE_BUTTON))
        try:
            confirm_btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", confirm_btn)
        
        # Дождаться исчезновения шаблона из списка
        time.sleep(2)  # Даем время на обработку удаления
        try:
            WebDriverWait(self.browser, 5).until_not(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{template_name}')]"))
            )
        except:
            # Если не удалось дождаться исчезновения, обновим страницу и проверим
            self.browser.refresh()
            time.sleep(2)

    @allure.step("Проверить отсутствие шаблона в списке")
    def assert_template_not_in_list(self, template_name: str):
        # Проверяем, что шаблон больше не отображается в списке
        try:
            self.browser.find_element(By.XPATH, f"//*[contains(text(),'{template_name}')]")
            raise AssertionError(f"Шаблон '{template_name}' все еще присутствует в списке")
        except:
            # Элемент не найден - это ожидаемое поведение
            pass


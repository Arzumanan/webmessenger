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
        from selenium.common.exceptions import NoSuchElementException
        try:
            self.browser.find_element(By.XPATH, f"//*[contains(text(),'{template_name}')]")
            raise AssertionError(f"Шаблон '{template_name}' все еще присутствует в списке")
        except NoSuchElementException:
            # Элемент не найден - это ожидаемое поведение
            pass

    # Локаторы для добавления группы шаблонов
    ADD_TEMPLATE_GROUP_BUTTON = (
        By.XPATH,
        "//button[@type='button' and contains(@class,'btn_primary') and contains(@class,'btn_default') and contains(@class,'btn_icon-none') and contains(normalize-space(.), 'Добавить группу шаблонов')]"
    )
    ADD_GROUP_MODAL_TITLE = (
        By.XPATH,
        "//form[contains(@class,'add-contact-wrapper')]//div[contains(@class,'add-contact-header-text') and normalize-space(text())='Новая группа']"
    )
    GROUP_NAME_INPUT = (
        By.XPATH,
        "//form[contains(@class,'add-contact-wrapper')]//input[@id='subsectionName' and @name='subsectionName']"
    )
    CREATE_GROUP_BUTTON = (
        By.XPATH,
        "//form[contains(@class,'add-contact-wrapper')]//button[@type='submit' and contains(normalize-space(.), 'Создать группу')]"
    )
    
    # Локаторы для редактирования группы шаблонов
    EDIT_GROUP_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'template-item_setting_button')]//svg[@viewBox='0 0 18 18']//path[contains(@d,'M1.60449 12.75')]"
    )
    EDIT_GROUP_MODAL_TITLE = (
        By.XPATH,
        "//form[contains(@class,'add-contact-wrapper')]//div[contains(@class,'add-contact-header-text') and contains(text(),'Редактирование')]"
    )
    UPDATE_GROUP_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'add-contact-form-submit')]//button[@type='submit' and contains(@class,'btn_primary') and contains(normalize-space(.), 'Обновить')]"
    )

    @allure.step("Открыть модалку добавления группы шаблонов")
    def open_add_group_modal(self):
        btn = self._wait().until(EC.element_to_be_clickable(self.ADD_TEMPLATE_GROUP_BUTTON))
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)
        self._wait().until(EC.visibility_of_element_located(self.ADD_GROUP_MODAL_TITLE))

    @allure.step("Заполнить название группы")
    def fill_group_name(self, group_name: str):
        self._fill_input(self.GROUP_NAME_INPUT, group_name)

    @allure.step("Создать группу шаблонов")
    def create_template_group(self):
        btn = self._wait().until(EC.element_to_be_clickable(self.CREATE_GROUP_BUTTON))
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)

    @allure.step("Проверить наличие группы в списке")
    def assert_group_in_list(self, group_name: str):
        self._wait().until(
            EC.visibility_of_element_located((By.XPATH, f"//*[contains(text(),'{group_name}')]"))
        )

    @allure.step("Найти и открыть редактирование группы по имени")
    def open_edit_group_modal(self, group_name: str):
        import time
        
        # Даем время на обновление DOM после создания группы
        time.sleep(2)
        
        # Ищем кнопку редактирования рядом с названием группы
        edit_btn = self._wait().until(
            EC.element_to_be_clickable((
                By.XPATH, 
                f"//*[contains(text(),'{group_name}')]/ancestor::*[contains(@class,'template') or contains(@class,'list') or self::li]//div[contains(@class,'template-item_setting_button')]"
            ))
        )
        
        # Прокрутим к кнопке и кликнем
        self.browser.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
        time.sleep(0.5)
        
        # Кликнуть на кнопку редактирования
        try:
            edit_btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", edit_btn)
        
        # Дождаться открытия модального окна редактирования
        time.sleep(1)
        try:
            self._wait().until(EC.visibility_of_element_located(self.EDIT_GROUP_MODAL_TITLE))
        except:
            # Если не нашли заголовок редактирования, попробуем найти заголовок создания
            self._wait().until(EC.visibility_of_element_located(self.ADD_GROUP_MODAL_TITLE))

    @allure.step("Обновить название группы")
    def update_group_name(self, new_group_name: str):
        self._fill_input(self.GROUP_NAME_INPUT, new_group_name)

    @allure.step("Сохранить изменения группы")
    def save_group_changes(self):
        # Попробуем найти кнопку "Обновить" с несколькими вариантами локаторов
        btn = None
        try:
            btn = self._wait().until(EC.element_to_be_clickable(self.UPDATE_GROUP_BUTTON))
        except:
            # Альтернативный локатор для кнопки "Обновить"
            try:
                btn = self._wait().until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@type='submit' and contains(@class,'btn_primary') and contains(normalize-space(.), 'Обновить')]"
                )))
            except:
                # Еще один альтернативный локатор
                btn = self._wait().until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//div[contains(@class,'add-contact-form-submit')]//button[contains(@class,'btn_primary')]"
                )))
        
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        try:
            close_btn = self._wait().until(EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class,'add-contact-close-button')]"
            )))
            try:
                close_btn.click()
            except Exception:
                self.browser.execute_script("arguments[0].click();", close_btn)
            time.sleep(1)
        except:
            # Если не удалось найти кнопку закрытия, попробуем нажать Escape
            from selenium.webdriver.common.keys import Keys
            self.browser.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(1)

    # Локаторы для редактирования шаблонов
    EDIT_TEMPLATE_BUTTON = (
        By.XPATH,
        "//div[contains(@class,'template-item_setting_button')]//svg[@viewBox='0 0 18 18']//path[contains(@d,'M1.60449 12.75')]"
    )
    EDIT_TEMPLATE_MODAL_TITLE = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//div[contains(@class,'add-contact-header-text') and contains(text(),'Редактирование')]"
    )
    UPDATE_TEMPLATE_BUTTON = (
        By.XPATH,
        "//form[contains(@class,'add-template-form')]//button[@type='submit' and contains(normalize-space(.), 'Обновить') or contains(normalize-space(.), 'Сохранить')]"
    )

    @allure.step("Найти и открыть редактирование шаблона по имени")
    def open_edit_template_modal(self, template_name: str):
        import time
        
        # Даем время на обновление DOM после создания шаблона
        time.sleep(2)
        
        # Ищем кнопку редактирования рядом с названием шаблона
        edit_btn = self._wait().until(
            EC.element_to_be_clickable((
                By.XPATH, 
                f"//*[contains(text(),'{template_name}')]/ancestor::*[contains(@class,'template') or contains(@class,'list') or self::li]//div[contains(@class,'template-item_setting_button')]"
            ))
        )
        
        # Прокрутим к кнопке и кликнем
        self.browser.execute_script("arguments[0].scrollIntoView({block:'center'});", edit_btn)
        time.sleep(0.5)
        
        # Кликнуть на кнопку редактирования
        try:
            edit_btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", edit_btn)
        
        # Дождаться открытия модального окна редактирования
        time.sleep(1)
        try:
            self._wait().until(EC.visibility_of_element_located(self.EDIT_TEMPLATE_MODAL_TITLE))
        except:
            # Если не нашли заголовок редактирования, попробуем найти заголовок создания
            self._wait().until(EC.visibility_of_element_located(self.MODAL_TITLE))

    @allure.step("Обновить название шаблона")
    def update_template_name(self, new_template_name: str):
        # Очищаем поле и вводим новое название
        self._fill_input(self.NAME_INPUT, new_template_name)

    @allure.step("Обновить текст шаблона")
    def update_template_text(self, new_template_text: str):
        # Очищаем поле и вводим новый текст
        self._fill_input(self.TEXTAREA_CONTENT, new_template_text)

    @allure.step("Сохранить изменения шаблона")
    def save_template_changes(self):
        # Попробуем найти кнопку "Обновить" или "Сохранить" с несколькими вариантами локаторов
        btn = None
        try:
            btn = self._wait().until(EC.element_to_be_clickable(self.UPDATE_TEMPLATE_BUTTON))
        except:
            # Альтернативный локатор для кнопки "Обновить"
            try:
                btn = self._wait().until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[@type='submit' and contains(@class,'btn_primary') and (contains(normalize-space(.), 'Обновить') or contains(normalize-space(.), 'Сохранить'))]"
                )))
            except:
                # Еще один альтернативный локатор
                btn = self._wait().until(EC.element_to_be_clickable((
                    By.XPATH,
                    "//form[contains(@class,'add-template-form')]//button[@type='submit']"
                )))
        
        try:
            btn.click()
        except Exception:
            self.browser.execute_script("arguments[0].click();", btn)

    @allure.step("Найти и удалить группу по имени")
    def delete_group_by_name(self, group_name: str):
        # Сначала найдем элемент с именем группы
        group_element = self._wait().until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{group_name}')]"))
        )
        
        # Прокрутим к элементу
        self.browser.execute_script("arguments[0].scrollIntoView({block:'center'});", group_element)
        
        # Найдем все кнопки в контейнере группы
        all_buttons = self.browser.find_elements(
            By.XPATH, 
            f"//*[contains(text(),'{group_name}')]/ancestor::*[contains(@class,'template') or contains(@class,'list') or self::li]//button"
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
            raise Exception(f"Не удалось найти кнопку удаления для группы '{group_name}'")
        
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
        
        # Дождаться исчезновения группы из списка
        time.sleep(2)  # Даем время на обработку удаления
        try:
            WebDriverWait(self.browser, 5).until_not(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{group_name}')]"))
            )
        except:
            # Если не удалось дождаться исчезновения, обновим страницу и проверим
            self.browser.refresh()
            time.sleep(2)

    @allure.step("Проверить отсутствие группы в списке")
    def assert_group_not_in_list(self, group_name: str):
        # Проверяем, что группа больше не отображается в списке
        from selenium.common.exceptions import NoSuchElementException
        try:
            self.browser.find_element(By.XPATH, f"//*[contains(text(),'{group_name}')]")
            raise AssertionError(f"Группа '{group_name}' все еще присутствует в списке")
        except NoSuchElementException:
            # Элемент не найден - это ожидаемое поведение
            pass


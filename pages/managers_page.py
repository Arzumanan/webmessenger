import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ManagersPage:
    """Page Object для раздела Менеджеры: добавление и удаление менеджера."""

    MODAL_FORM = "//form[contains(@class,'add-manager-form')]"

    # Локаторы навигации
    MANAGERS_SIDEBAR_LINK = (By.ID, "managers")
    ADD_MANAGER_BUTTON = (By.XPATH, "//button[contains(@class, 'manager-sidebar-add-manager-btn') and contains(text(),'Добавить менеджера')]")

    # Локаторы модалки добавления
    NAME_INPUT = (By.XPATH, f"{MODAL_FORM}//input[@id='username']")
    EMAIL_INPUT = (By.XPATH, f"{MODAL_FORM}//input[@id='email']")
    PASSWORD_INPUT = (By.XPATH, f"{MODAL_FORM}//input[@id='password']")
    REPEAT_PASSWORD_INPUT = (By.XPATH, f"{MODAL_FORM}//input[@id='repeatPassword']")
    SUBMIT_ADD_BUTTON = (By.XPATH, f"{MODAL_FORM}//button[@type='submit' and contains(.,'Добавить')]")
    MODAL_TITLE = (By.XPATH, "//p[contains(@class,'modal__title') and text()='Добавление менеджера']")

    # Кнопка удаления в форме редактирования справа
    DELETE_BUTTON_FORM = (By.XPATH, "//button[contains(@class,'edit-manager-form__btn_delete')]")
    DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[contains(@class,'delete-manager-modal__btn') and contains(.,'Удалить')]")

    def __init__(self, driver, wait_timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)

    def navigate_to_managers_section(self):
        """Переход в раздел Менеджеры"""
        managers_link = self.wait.until(EC.element_to_be_clickable(self.MANAGERS_SIDEBAR_LINK))
        managers_link.click()
        time.sleep(2)  # Небольшая пауза для загрузки

    def open_add_manager_modal(self):
        """Открытие модального окна добавления менеджера"""
        add_button = self.wait.until(EC.element_to_be_clickable(self.ADD_MANAGER_BUTTON))
        add_button.click()

    def wait_modal_opened(self):
        self.wait.until(EC.visibility_of_element_located(self.MODAL_TITLE))

    def fill_input(self, locator, value):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        try:
            element.click(); time.sleep(0.05)
            element.clear(); time.sleep(0.05)
            element.send_keys(value)
        except Exception:
            self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", element)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles:true}));", element)

    def fill_passwords(self, password: str):
        # Берем видимый input внутри формы (на странице два input с одинаковым id)
        pw_candidates = self.driver.find_elements(*self.PASSWORD_INPUT)
        password_input = None
        for el in pw_candidates:
            try:
                if el.is_displayed():
                    password_input = el
                    break
            except Exception:
                continue
        if password_input is None:
            password_input = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))

        try:
            password_input.click(); time.sleep(0.05)
            password_input.clear(); time.sleep(0.05)
            password_input.send_keys(password)
        except Exception:
            self.driver.execute_script("arguments[0].value = arguments[1];", password_input, password)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", password_input)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles:true}));", password_input)

        # Повтор пароля
        rpw_candidates = self.driver.find_elements(*self.REPEAT_PASSWORD_INPUT)
        repeat_input = None
        for el in rpw_candidates:
            try:
                if el.is_displayed():
                    repeat_input = el
                    break
            except Exception:
                continue
        if repeat_input is None:
            repeat_input = self.wait.until(EC.visibility_of_element_located(self.REPEAT_PASSWORD_INPUT))

        try:
            repeat_input.click(); time.sleep(0.05)
            repeat_input.clear(); time.sleep(0.05)
            repeat_input.send_keys(password)
        except Exception:
            self.driver.execute_script("arguments[0].value = arguments[1];", repeat_input, password)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles:true}));", repeat_input)
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles:true}));", repeat_input)

        # Верифицируем
        WebDriverWait(self.driver, 5).until(
            lambda d: password_input.get_attribute('value') == password and repeat_input.get_attribute('value') == password
        )

    def submit_add(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_ADD_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

    def wait_modal_closed(self):
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.MODAL_TITLE)
        )

    def select_in_sidebar_by_email(self, email: str):
        item = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(),'{email}')]") ))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", item)
        try:
            item.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", item)

    def click_delete_in_form(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.DELETE_BUTTON_FORM))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

    def confirm_delete_modal(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.DELETE_CONFIRM_BUTTON))
        try:
            btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", btn)

    def wait_removed_from_list(self, email: str):
        WebDriverWait(self.driver, 15).until_not(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{email}')]"))
        )

    def add_manager(self, name: str, email: str, password: str):
        """Заполнение модалки и сабмит."""
        self.wait_modal_opened()
        self.fill_input(self.NAME_INPUT, name)
        self.fill_input(self.EMAIL_INPUT, email)
        self.fill_passwords(password)
        self.submit_add()
        try:
            self.wait_modal_closed()
        except Exception:
            # если модалка быстро исчезла или осталась — продолжаем
            pass

    def delete_manager(self, email: str):
        self.select_in_sidebar_by_email(email)
        self.click_delete_in_form()
        self.confirm_delete_modal()
        self.wait_removed_from_list(email)

    def create_new_manager(self, name: str, email: str, password: str):
        """Полный процесс создания нового менеджера"""
        self.navigate_to_managers_section()
        self.open_add_manager_modal()
        self.add_manager(name, email, password)
        
        # Проверяем, что менеджер появился в списке
        created_manager = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//*[contains(text(),'{email}')]"))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", created_manager)
        return email



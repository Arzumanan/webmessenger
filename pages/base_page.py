import allure
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait  # Импорт WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import browser
from config.links import Links


class BasePage:
    def __init__(self, browser):
        self.browser: WebDriver = browser
        self.wait = WebDriverWait(browser, 10)

    @allure.step("Открытие страницы")
    def open(self):
        return self.browser.get(self.PAGE_URL)

    def open_host(self):
        return self.browser.get(Links.HOST)

    def element_in_visible(self, locator, timeout=10):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def elements_in_visible(self, locator, timeout=10):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def element_in_clickable(self, locator, timeout=10):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def element_in_localed(self, locator, timeout=10):
        return self.wait.until(EC.presence_of_element_located(locator))

    def element_is_not_visible(self, locator, timeout=10):
        return self.wait.until_not(EC.visibility_of_element_located(locator))

    def find_element(self, locator):
        return self.browser.find_element(locator)

    def dismiss_notifications_banner(self):
        """Закрытие баннера уведомлений если он появился"""
        import time
        try:
            deny = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((
                By.XPATH,
                '//*[self::button or self::a][contains(., "Не сейчас") or contains(., "Позже") or contains(., "Запретить") or contains(., "Не разрешать") or contains(., "Закрыть")]'
            )))
            self.browser.execute_script("arguments[0].scrollIntoView({block:'center'});", deny)
            time.sleep(0.3)
            try:
                deny.click()
            except Exception:
                self.browser.execute_script("arguments[0].click();", deny)
        except Exception:
            # Альтернатива: закрытие по иконке крестика
            try:
                close_btn = WebDriverWait(self.browser, 3).until(EC.element_to_be_clickable((
                    By.XPATH,
                    '//*[contains(@class, "close") or contains(@class, "icon-close")][self::button or self::span or self::i]'
                )))
                try:
                    close_btn.click()
                except Exception:
                    self.browser.execute_script("arguments[0].click();", close_btn)
            except Exception:
                pass



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
    # 1


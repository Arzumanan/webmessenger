import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait



@pytest.fixture(scope="function", autouse=False)
def browser(request):
    options = Options()
    # options.add_argument("--headless") # режим запуска теста без визуального открытия браузера.
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Включаем JavaScript (не отключаем), иначе SPA/форма логина не работает
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)  # Используем опции
    # Привязываем драйвер к классу теста, если он есть (для функциональных тестов request.cls = None)
    if getattr(request, "cls", None) is not None:
        request.cls.driver = driver
    yield driver  # Выход из фикстуры, передача браузера в тест
    driver.quit()  # Закрытие браузера после завершения теста

@pytest.fixture(scope="function")
def admin_authorized(browser):
    from pages.login_admin_page import LoginAdminPage
    from cookie.cookies import load_cookies, save_cookies
    from config.data import admin_email, admin_password
    # Пытаемся восстановить сессию по куки
    if load_cookies(browser):
        return browser

    # Если куки нет — логинимся и сохраняем
    page = LoginAdminPage(browser)
    page.open_host()
    page.open_admin_login_page()
    page.enter_email(admin_email)
    page.enter_password(admin_password)
    page.admin_authorization()
    WebDriverWait(browser, 15).until(lambda d: "/login" not in d.current_url)
    save_cookies(browser)
    return browser
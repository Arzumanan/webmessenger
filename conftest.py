import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



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
"""Модуль для работы с cookies браузера."""
import os
import pickle
from config.links import Links


def save_cookies(driver, path="cookies/cookies.pkl"):
    """
    Сохраняет cookies браузера в файл.
    
    Args:
        driver: WebDriver экземпляр
        path (str): Путь к файлу для сохранения cookies
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, url=Links.HOST, path="cookies/cookies.pkl"):
    """
    Загружает cookies из файла в браузер.
    
    Args:
        driver: WebDriver экземпляр
        url (str): URL для загрузки перед установкой cookies
        path (str): Путь к файлу с cookies
        
    Returns:
        bool: True если cookies загружены успешно, False если файл не найден
    """
    if not os.path.exists(path):
        return False
        
    driver.get(url)
    
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        
    for cookie in cookies:
        cookie.pop("sameSite", None)
        if "expiry" in cookie and isinstance(cookie["expiry"], float):
            cookie["expiry"] = int(cookie["expiry"])
        try:
            driver.add_cookie(cookie)
        except Exception:
            pass
            
    driver.refresh()
    return True
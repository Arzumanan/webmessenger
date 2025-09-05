import allure
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.links import Links
from pages.base_page import BasePage


class TagsPage(BasePage):
    PAGE_URL = "https://testim.i2crm.ru/tags-statuses"

    # Локаторы для кнопок и полей
    ADD_TAG_BUTTON = ("xpath", "//button[contains(@class, 'tags-status-settings__add-btn') and contains(text(), '+ Добавить тег')]")
    TAG_INPUT_FIELD = ("xpath", "//input[@class='add-contact-form-control-input' and @placeholder='Текст']")
    SUBMIT_ADD_TAG_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and contains(text(), 'Добавить тег')]")
    
    # Локаторы для редактирования и удаления тегов
    EDIT_TAG_ICON = ("xpath", "//svg[@class='tag-item-icon']//path[contains(@d, 'M9.244 1.8125')]")
    DELETE_TAG_ICON = ("xpath", "//svg[@class='tag-item-icon']//path[contains(@d, 'M2.1875 3.41663')]")
    
    # Локаторы для модального окна редактирования
    EDIT_TAG_INPUT = ("xpath", "//input[@class='add-contact-form-control-input']")
    SAVE_EDIT_BUTTON = ("xpath", "//button[@class='btn btn_primary btn_default btn_icon-none' and contains(text(), 'Сохранить')]")
    
    # Локаторы для подтверждения редактирования
    CONFIRM_EDIT_BUTTON = ("xpath", "//div[@class='warning_wrapper']//button[contains(text(), 'Да')]")
    
    # Локаторы для подтверждения удаления
    CONFIRM_DELETE_BUTTON = ("xpath", "//button[contains(@class, 'btn_primary') and contains(text(), 'Удалить')]")

    @allure.step("Открытие страницы тегов")
    def open_tags_page(self):
        """Открытие страницы тегов"""
        self.browser.get(self.PAGE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    @allure.step("Нажатие на кнопку 'Добавить тег'")
    def click_add_tag_button(self):
        """Нажатие на кнопку добавления тега"""
        add_button = self.element_in_clickable(self.ADD_TAG_BUTTON)
        add_button.click()

    @allure.step("Заполнение поля ввода тега")
    def fill_tag_input(self, tag_text):
        """Заполнение поля ввода тега"""
        tag_input = self.element_in_clickable(self.TAG_INPUT_FIELD)
        tag_input.clear()
        tag_input.send_keys(tag_text)

    @allure.step("Нажатие на кнопку 'Добавить тег' для сохранения")
    def click_submit_add_tag(self):
        """Нажатие на кнопку сохранения тега"""
        submit_button = self.element_in_clickable(self.SUBMIT_ADD_TAG_BUTTON)
        submit_button.click()

    @allure.step("Создание нового тега")
    def create_tag(self, tag_text):
        """Полный процесс создания тега"""
        self.click_add_tag_button()
        self.fill_tag_input(tag_text)
        self.click_submit_add_tag()
        
        # Ждем, пока тег появится на странице
        import time
        time.sleep(1)  # Даем время на обновление страницы

    @allure.step("Генерация случайного тега")
    def generate_random_tag(self, min_length=4, max_length=17):
        """Генерация случайного тега заданной длины"""
        length = random.randint(min_length, max_length)
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @allure.step("Поиск тега по тексту")
    def find_tag_by_text(self, tag_text):
        """Поиск тега по тексту"""
        # Ищем по точной структуре HTML
        locators = [
            f"//span[@class='tag-item_title' and text()='{tag_text}']",
            f"//span[@class='tag-item_title' and contains(text(), '{tag_text}')]",
            f"//li[@class='tag-item']//span[@class='tag-item_title' and text()='{tag_text}']",
            f"//li[@class='tag-item']//span[@class='tag-item_title' and contains(text(), '{tag_text}')]"
        ]
        
        for xpath in locators:
            try:
                elements = self.browser.find_elements(By.XPATH, xpath)
                if elements:
                    return elements[0]
            except:
                continue
        
        return None

    @allure.step("Редактирование тега")
    def edit_tag(self, old_text, new_text):
        """Редактирование существующего тега"""
        # Находим тег
        tag_element = self.find_tag_by_text(old_text)
        if not tag_element:
            raise Exception(f"Тег '{old_text}' не найден")
        
        # Находим родительский li элемент
        li_element = tag_element.find_element(By.XPATH, "./ancestor::li[@class='tag-item']")
        
        # Пробуем разные варианты поиска иконки редактирования
        edit_icon = None
        icon_selectors = [
            ".//div[@class='tag-item_block']//svg[@class='tag-item-icon'][1]",
            ".//svg[@class='tag-item-icon'][1]",
            ".//svg[contains(@class, 'tag-item-icon')][1]",
            ".//*[contains(@class, 'tag-item-icon')][1]"
        ]
        
        for selector in icon_selectors:
            try:
                edit_icon = li_element.find_element(By.XPATH, selector)
                break
            except:
                continue
        
        if not edit_icon:
            raise Exception(f"Не удалось найти иконку редактирования для тега '{old_text}'")
        
        edit_icon.click()
        
        # Подтверждаем редактирование в модальном окне
        confirm_button = self.element_in_clickable(self.CONFIRM_EDIT_BUTTON, timeout=5)
        confirm_button.click()
        
        # Заполняем новое значение
        edit_input = self.element_in_clickable(self.EDIT_TAG_INPUT, timeout=5)
        edit_input.clear()
        edit_input.send_keys(new_text)
        
        # Пробуем разные варианты поиска кнопки сохранения
        save_button = None
        save_selectors = [
            "//button[@class='btn btn_primary btn_default btn_icon-none' and contains(text(), 'Сохранить')]",
            "//button[contains(@class, 'btn_primary') and contains(text(), 'Сохранить')]",
            "//button[contains(text(), 'Сохранить')]",
            "//button[@type='button' and contains(text(), 'Сохранить')]"
        ]
        
        for selector in save_selectors:
            try:
                save_button = self.element_in_clickable((By.XPATH, selector), timeout=3)
                break
            except:
                continue
        
        if not save_button:
            raise Exception(f"Не удалось найти кнопку 'Сохранить' для тега '{old_text}'")
        
        save_button.click()
        
        # Ждем, пока тег обновится на странице
        import time
        time.sleep(2)  # Даем больше времени на обновление

    @allure.step("Удаление тега")
    def delete_tag(self, tag_text):
        """Удаление тега с умным парсером"""
        print(f"Ищем тег для удаления: '{tag_text}'")
        
        # Получаем все теги на странице
        all_tags = self.get_all_tags_on_page()
        print(f"Все теги на странице: {all_tags}")
        
        # Ищем тег в списке
        if tag_text not in all_tags:
            raise Exception(f"Тег '{tag_text}' не найден на странице. Доступные теги: {all_tags}")
        
        # Находим все li элементы с тегами
        li_elements = self.browser.find_elements(By.XPATH, "//li[@class='tag-item']")
        print(f"Найдено {len(li_elements)} элементов тегов")
        
        target_li = None
        for li in li_elements:
            # Ищем span с текстом тега
            span_elements = li.find_elements(By.XPATH, ".//span[@class='tag-item_title']")
            for span in span_elements:
                if span.text.strip() == tag_text:
                    target_li = li
                    print(f"Найден тег '{tag_text}' в li элементе")
                    break
            if target_li:
                break
        
        if not target_li:
            raise Exception(f"Не удалось найти li элемент для тега '{tag_text}'")
        
        # Ищем иконку корзины (удаления) в найденном li элементе
        delete_icon = None
        
        # Способ 1: Ищем SVG с 5 path элементами (корзина)
        svg_elements = target_li.find_elements(By.XPATH, ".//svg[@class='tag-item-icon']")
        print(f"Найдено {len(svg_elements)} SVG иконок в li элементе")
        
        for i, svg in enumerate(svg_elements):
            paths = svg.find_elements(By.XPATH, ".//path")
            print(f"SVG {i+1}: {len(paths)} path элементов")
            
            # Корзина имеет 5 path элементов
            if len(paths) == 5:
                delete_icon = svg
                print(f"Найдена иконка корзины (SVG {i+1}) с {len(paths)} path элементами")
                break
        
        # Способ 2: Если не нашли по количеству path, берем вторую иконку
        if not delete_icon and len(svg_elements) >= 2:
            delete_icon = svg_elements[1]  # Вторая иконка
            print("Используем вторую иконку как иконку удаления")
        
        # Способ 3: Ищем по конкретному path корзины
        if not delete_icon:
            try:
                delete_icon = target_li.find_element(By.XPATH, ".//svg[@class='tag-item-icon']//path[starts-with(@d, 'M2.1875 3.41663')]")
                print("Найдена иконка корзины по path")
            except:
                pass
        
        if not delete_icon:
            raise Exception(f"Не удалось найти иконку удаления для тега '{tag_text}'")
        
        # Кликаем по иконке удаления
        print(f"Кликаем по иконке удаления для тега '{tag_text}'")
        delete_icon.click()
        
        # Подтверждаем удаление
        print("Подтверждаем удаление")
        confirm_button = self.element_in_clickable(self.CONFIRM_DELETE_BUTTON)
        confirm_button.click()
        
        # Ждем обновления страницы
        import time
        time.sleep(2)
        print(f"Тег '{tag_text}' удален")

    @allure.step("Проверка наличия тега")
    def is_tag_present(self, tag_text):
        """Проверка наличия тега на странице"""
        tag_element = self.find_tag_by_text(tag_text)
        return tag_element is not None

    @allure.step("Ожидание исчезновения тега")
    def wait_for_tag_disappear(self, tag_text, timeout=10):
        """Ожидание исчезновения тега"""
        # Ищем по точной структуре HTML
        locators = [
            (By.XPATH, f"//span[@class='tag-item_title' and text()='{tag_text}']"),
            (By.XPATH, f"//span[@class='tag-item_title' and contains(text(), '{tag_text}')]"),
            (By.XPATH, f"//li[@class='tag-item']//span[@class='tag-item_title' and text()='{tag_text}']")
        ]
        
        for locator in locators:
            try:
                self.wait.until_not(EC.visibility_of_element_located(locator), timeout=timeout)
                return True
            except:
                continue
        return False

    @allure.step("Отладка: получение всех тегов на странице")
    def get_all_tags_on_page(self):
        """Получение всех тегов на странице для отладки"""
        try:
            # Ищем все теги по точной структуре
            all_elements = self.browser.find_elements(By.XPATH, "//span[@class='tag-item_title']")
            tags = []
            for element in all_elements:
                text = element.text.strip()
                if text:
                    tags.append(text)
            return tags
        except:
            return []
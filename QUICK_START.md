# Быстрый старт - Тест скачивания Excel файла

## 1. Установка зависимостей

```bash
pip install pandas==2.0.3 openpyxl==3.1.2
```

## 2. Запуск простого примера

```bash
python test_excel_download_example.py
```

## 3. Запуск через pytest

```bash
# Запуск теста скачивания Excel
pytest tests/test_contacts.py::TestContacts::test_download_and_open_excel_file -v -s

# Запуск с выводом в консоль
pytest tests/test_contacts.py::TestContacts::test_download_and_open_excel_file -v -s --tb=short
```

## 4. Что делает тест

1. 🔐 Авторизуется в системе
2. 📄 Переходит на страницу контактов  
3. ⬇️ Скачивает Excel файл через кнопку `EXPORT_EXCEL_BUTTON`
4. ✅ Проверяет, что файл скачался и не пустой
5. 📊 Читает содержимое Excel файла
6. 🔍 Проверяет структуру данных
7. 🖥️ Открывает файл в системе

## 5. Результат

- Файл сохраняется в папку `downloads/`
- В консоли выводится информация о файле
- Excel файл автоматически открывается

## 6. Настройка

Если нужно изменить ожидаемые колонки, отредактируйте в тесте:

```python
expected_columns = ['Имя', 'Логин', 'Телефон', 'Канал']  # Ваши колонки
```

# Bailanysta

Bailanysta - это социальная сеть, разработанная на Django, с поддержкой мультиязычности и интеграцией с Gemini AI.

## Особенности

- Мультиязычный интерфейс (Русский, Английский, Казахский)
- Темная/светлая тема
- Интеграция с Gemini AI для генерации контента
- Система подписок и лайков
- Комментарии к постам
- Поиск по контенту
- Профили пользователей с аватарами

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/bailanysta.git
cd bailanysta
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта и добавьте следующие переменные:
```
GEMINI_API_KEY=your-gemini-api-key
DEBUG=True
SECRET_KEY=your-secret-key
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

7. Запустите сервер разработки:
```bash
python manage.py runserver
```

## Использование

1. Зарегистрируйтесь или войдите в систему
2. Создавайте посты, используя обычный ввод или генерацию с помощью AI
3. Взаимодействуйте с другими пользователями через систему подписок и лайков
4. Используйте поиск для нахождения интересного контента

## Технологии

- Django
- Bootstrap
- JavaScript
- Google Gemini AI API
- SQLite (для разработки)

## Лицензия

MIT 
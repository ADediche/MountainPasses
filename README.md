# MountainPasses

**MountainPasses** — это приложение для управления данными о горных перевалах. API позволяет создавать, получать, редактировать и фильтровать записи о перевалах, включая информацию о пользователях, координатах, уровнях сложности и изображениях. 

## Основные возможности

- **Создание перевала**: POST `/submitData/` для добавления нового перевала с данными пользователя, координатами, уровнями сложности и изображениями.
- **Получение данных**:
  - GET `/submitData/<id>/` — получение перевала по ID.
  - GET `/submitData/?user__email=<email>` — список перевалов по email пользователя.
- **Редактирование перевала**: PATCH `/submitData/<id>/` для обновления перевала (доступно только для статуса `new`).
- **Swagger UI**: Интерактивная документация API доступна по `/swagger/`.
- **Тестирование**: тесты, проверяющие функционал API и обработку ошибок.

## Технологии

- **Backend**: Django 5.2, Django REST Framework 3.16
- **База данных**: PostgreSQL (SQLite для тестов)
- **Документация**: drf-yasg 1.21.10 (Swagger UI)
- **Тестирование**: pytest, pytest-django, pytest-cov

## Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://https://github.com/ADediche/MountainPasses.git
   cd MountainPasses
   ```

2. **Создайте виртуальное окружение**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\scripts\activate  # Windows
   ```

3. **Установите зависимости**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте окружение**:
   Создайте файл `.env` в корне проекта:
   ```
   DJANGO_SECRET_KEY=ваш-секретный-ключ
   DB_NAME=имя-базы-данных
   USER=ваш-логин
   DB_PASSWORD=ваш-пароль
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Настройте базу данных**:
   ```bash
   python manage.py migrate
   ```

6. **Соберите статические файлы**:
   ```bash
   python manage.py collectstatic --noinput
   ```

7. **Запустите сервер**:
   ```bash
   python manage.py runserver
   ```

## Использование

- **API**: Доступно по `http://127.0.0.1:8000/`.
- **Swagger UI**: Откройте `http://127.0.0.1:8000/swagger/` для просмотра и тестирования эндпоинтов.
- **Пример POST-запроса**:
  ```json
  {
    "data": "{\"user\": {\"email\": \"test@example.com\", \"first_name\": \"John\", \"last_name\": \"Doe\", \"phone\": \"+1234567890\"}, \"area\": {\"title\": \"Test Area\"}, \"pereval\": {\"title\": \"Test Pereval\", \"coords\": {\"latitude\": 45.0, \"longitude\": 7.0, \"height\": 1200}, \"level\": {\"winter\": \"1А\", \"summer\": \"\", \"autumn\": \"\", \"spring\": \"\"}, \"images\": [{\"title\": \"Image 1\"}]}}",
    "images": "<файл изображения>"
  }
  ```
  Ответ: `{"status": 200, "message": "", "id": 1}`

## Документация

- **Swagger UI**: `http://127.0.0.1:8000/swagger/` — интерактивная документация с описанием эндпоинтов, параметров и примеров ответов.

## Контакты

- **Автор**: Alekei Dedichenko
- **Email**: dedichenkoa@gmail.com
- **GitHub**: https://github.com/ADediche

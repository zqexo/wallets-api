# Wallets API

Этот проект представляет приложение для управления кошельками пользователей. Он включает API-интерфейс для создания, получения и удаления кошельков, а также выполнения операций пополнения и снятия средств с кошельков.

## 📋 Описание проекта
Особенности:

- Кошельки: возможность создания кошельков для пользователей с балансом.
- Операции с кошельками: поддержка операций пополнения и снятия средств.
- API:
  - CRUD для всех сущностей (кошельки).
  - Операции с кошельками (пополнение, снятие).
  - Фильтрация кошельков по UUID.
  - Защита от недопустимых запросов (например, недостаточно средств или неверный формат данных).
  - Обработка ошибок с понятными сообщениями для пользователя.
  - Высокая производительность при работе в условиях высокой нагрузки (1000 RPS по одному кошельку).

Дополнительно:

- Документация API: доступна через Swagger и ReDoc.
- Поддержка CORS для работы с внешними клиентами.

---

## 📂 Структура проекта
```users/``` — Приложение для управления пользователями.\
```wallets/``` — Приложение для работы с кошельками.\
```Wallets.postman_collection.json``` — Коллекция Postman запросов.

```
Demo/
├── Demo/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── wallets/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
├── .env
├── .env.docker
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── wallets.postman_collection.json
├── README.md

```

---

## 🛠️ Технологии

- **Backend:** Python 3.11, Django 5+, Django REST Framework.
- **База данных:** PostgreSQL.
- **Документация:** DRF-yasg.
- **Контейнеризация:** Docker, Docker Compose.

---

## 🚀 Установка и запуск

### 1. Склонируйте репозиторий
```bash

git clone https://github.com/zqexo/wallets-api.git
cd wallets-api
```
### 2. Настройте переменные окружения
Создайте файл .env.docker в корне проекта со следующим содержимым:
```
SECRET_KEY=
DEBUG=

CORS_ALLOW_ALL_ORIGINS=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```
### 3. Соберите и запустите контейнеры
- Сборка и запуск контейнеров:
```bash

docker-compose up --build
```
- Остановка контейнеров:
```bash

docker-compose down
```
- Создать суперпользователя:
```bash

docker-compose exec app python manage.py csu
```

### 4. Полезные ссылки

Админ-панель: ```http://localhost:8000/admin/``` \
Swagger-документация: ```http://localhost:8000/swagger/``` \
ReDoc-документация: ```http://localhost:8000/redoc/```

---

## 🧪 Тестирование

1. Установите Postman.
2. Импортируйте коллекцию Postman из репозитория.
3. Выполните тестовые запросы к API.

---

## 📞 Контакты

- #### Telegram: ```@zqexo```
  - #### Email: ```z@qexo.ru```
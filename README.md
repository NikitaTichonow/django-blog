<div align="center">

# Django Blog

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.0%2B-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.12%2B-red)](https://www.django-rest-framework.org/)

</div>

## 📝 О проекте

Django Blog - это современная блог-платформа, разработанная с использованием Django и Django Rest Framework. Проект предоставляет полноценный функционал для ведения блога с поддержкой мультиязычности.

### 🔑 Основные возможности

- 👤 **Система пользователей**:
  - Регистрация и авторизация
  - Личный кабинет
  - Управление профилем

- 📝 **Управление записями**:
  - Создание и редактирование постов (для администраторов)
  - Просмотр записей
  - Комментирование постов

- 🌐 **API Интерфейс**:
  - RESTful API для всех функций
  - Документация API (Swagger/ReDoc)

- 🔄 **Дополнительно**:
  - Мультиязычность
  - Асинхронные задачи (Celery)
  - Мониторинг задач (Flower)

## 🚀 Установка и запуск

### Предварительные требования

- Python 3.8+
- Redis (для Celery)
- Git

### Шаги установки

1. **Клонирование репозитория:**
```bash
git clone https://github.com/NikitaTichonow/django-blog
cd django-blog
```

2. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

3. **Настройка окружения:**
- Создайте файл `.env` на основе `.env.template`
- Заполните необходимые переменные окружения:
```env
SECRET_KEY_ENV="ваш_секретный_ключ"
```

4. **Применение миграций:**
```bash
python manage.py migrate
```

5. **Запуск сервера разработки:**
```bash
python manage.py runserver
```

### Запуск фоновых задач

1. **Запуск Redis:**
```bash
redis-server
```

2. **Запуск Celery (для Windows):**
```bash
celery -A django_blog worker -l info --pool=solo
```

3. **Запуск Celery Beat:**
```bash
celery -A django_blog beat -l info
```

4. **Запуск Flower для мониторинга:**
```bash
celery -A django_blog flower
```
- **Flower:** `http://localhost:5555/`

## 📚 API Документация

- **Swagger UI:** `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://127.0.0.1:8000/api/schema/redoc/`

### Основные эндпоинты

- **Список пользователей (админ):** `http://127.0.0.1:8000/api/profile_list/`
- **Список постов (админ):** `http://127.0.0.1:8000/api/post_list/`

## 🤝 Вклад в проект

Если вы хотите внести свой вклад в проект:

1. Сделайте форк репозитория
2. Создайте ветку для своей функции
3. Внесите изменения и создайте pull request



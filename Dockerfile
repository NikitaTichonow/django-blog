# Используем официальный образ Python
FROM python:3.8-slim

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание директории для статических файлов
RUN mkdir -p /app/static

# Порт
EXPOSE 8000

# Запуск сервера
CMD ["python", "django_blog/manage.py", "runserver", "0.0.0.0:8000"]
import os
import pytest
from django.conf import settings

#PostgreSQL 
@pytest.mark.django_db

# Проверяет, что параметры конфигурации базы данных совпадают с ожидаемыми значениями из переменных окружения.
def test_datebase_configuration():
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql"
    assert settings.DATABASES["default"]["NAME"] == 'test_blog'
    assert settings.DATABASES["default"]["USER"] == str(os.getenv("USER_POSTGRES"))
    assert settings.DATABASES["default"]["PASSWORD"] == str(os.getenv("PASSWORD_POSTGRES"))
    assert settings.DATABASES["default"]["HOST"] == str(os.getenv("HOST_POSTGRES"))
    assert settings.DATABASES["default"]["PORT"] == str(os.getenv("PORT_POSTGRES"))

# Проверяет, может ли приложение подключиться к базе данных и что соединение активно.
@pytest.mark.django_db
def test_database_connection(client):
    from django.db import connection

    try:
        connection.ensure_connection()
        assert connection.is_usable() is True
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

#Проверяет, что все необходимые переменные окружения заданы и не равны None.
@pytest.mark.django_db
def test_environment_variables():
    assert os.getenv("NAME_POSTGRES") is not None
    assert os.getenv("USER_POSTGRES") is not None
    assert os.getenv("PASSWORD_POSTGRES") is not None
    assert os.getenv("HOST_POSTGRES") is not None
    assert os.getenv("PORT_POSTGRES") is not None


# SQlite

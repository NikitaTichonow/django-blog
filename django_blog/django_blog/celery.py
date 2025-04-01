from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную окружения для Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_blog.settings")

app = Celery("django_blog")

# Загрузите настройки из Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически найдите задачи в приложениях Django
app.autodiscover_tasks()

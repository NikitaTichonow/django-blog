import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')

app = Celery('django_blog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Настройка периодических задач
app.conf.beat_schedule = {
    'cleanup-old-posts': {
        'task': 'apps.blog.tasks.cleanup_old_posts',
        'schedule': crontab(hour=0, minute=0),  # Выполнять каждый день в полночь
    },
    'send-weekly-digest': {
        'task': 'apps.blog.tasks.send_weekly_digest',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),  # Каждый понедельник в 8:00
    },
    'generate-activity-report': {
        'task': 'apps.blog.tasks.generate_activity_report',
        'schedule': crontab(hour=23, minute=59),  # Каждый день в 23:59
    },
    'notify-users-about-new-posts': {
        'task': 'apps.blog.tasks.notify_users_about_new_posts',
        'schedule': crontab(hour='*/6', minute=0),  # Каждые 6 часов
    },
    'check-blog-status-every-minute': {
        'task': 'apps.blog.tasks.check_blog_status',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
    'check-database-connection': {
        'task': 'apps.blog.tasks.check_database_connection',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}
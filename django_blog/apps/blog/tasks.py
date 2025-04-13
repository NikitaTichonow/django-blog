from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth import get_user_model
from datetime import timedelta
from .models import Post, Comment

@shared_task
def cleanup_old_posts():
    """Удаление постов старше 1 года, которые не имеют комментариев и лайков"""
    threshold_date = timezone.now() - timedelta(days=365)
    old_posts = Post.objects.filter(
        created__lt=threshold_date,
        comments__isnull=True
    ).delete()
    return f'Удалено {old_posts[0]} старых постов'

@shared_task
def send_weekly_digest():
    """Отправка еженедельного дайджеста с популярными постами"""
    week_ago = timezone.now() - timedelta(days=7)
    popular_posts = Post.objects.filter(
        created__gte=week_ago
    ).order_by('-views')[:5]

    if popular_posts:
        subject = 'Еженедельный дайджест популярных постов'
        message = 'Топ постов за неделю:\n\n'
        for post in popular_posts:
            message += f'- {post.title} (Просмотров: {post.views})\n'

        User = get_user_model()
        recipient_list = User.objects.filter(is_active=True).values_list('email', flat=True)
        
        send_mail(
            subject,
            message,
            'noreply@example.com',
            recipient_list,
            fail_silently=True,
        )
        return 'Дайджест успешно отправлен'
    return 'Нет популярных постов для отправки'

@shared_task
def generate_activity_report():
    """Генерация отчета об активности на сайте"""
    today = timezone.now()
    yesterday = today - timedelta(days=1)
    
    new_posts = Post.objects.filter(created__gte=yesterday).count()
    new_comments = Comment.objects.filter(created__gte=yesterday).count()
    
    report = f'Отчет об активности за {yesterday.strftime("%Y-%m-%d")}:\n'
    report += f'Новых постов: {new_posts}\n'
    report += f'Новых комментариев: {new_comments}\n'
    
    # Можно сохранить отчет в файл или отправить администратору
    return report

@shared_task
def notify_users_about_new_posts():
    """Отправляет уведомления пользователям о новых постах за последние 24 часа."""
    # Получаем посты за последние 24 часа
    last_day = timezone.now() - timedelta(days=1)
    new_posts = Post.objects.filter(created__gte=last_day, status='published')
    
    if not new_posts.exists():
        return "Нет новых постов для уведомления"
    
    # Получаем всех активных пользователей
    User = get_user_model()
    users = User.objects.filter(is_active=True)
    
    # Формируем список писем
    emails = []
    for user in users:
        if user.email:  # Проверяем наличие email
            subject = 'Новые посты в блоге'
            message = f'Здравствуйте, {user.username}!\n\nЗа последние 24 часа появились новые посты:\n\n'
            
            for post in new_posts:
                message += f'- {post.title}\n'
            
            message += '\nПосетите наш сайт, чтобы прочитать их!'
            
            # Добавляем письмо в список
            emails.append((
                subject,
                message,
                'noreply@example.com',  # От кого
                [user.email]  # Кому
            ))
    
    # Отправляем все письма
    if emails:
        send_mass_mail(emails, fail_silently=False)
        return f"Отправлено {len(emails)} уведомлений о {new_posts.count()} новых постах"
    
    return "Нет пользователей для уведомления"
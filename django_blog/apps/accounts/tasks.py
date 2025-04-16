import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

@shared_task
def send_verification_email(user_id, email):
    """Отправка кода подтверждения на email"""
    from .models import Profile
    
    # Генерация 6-значного кода
    verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # Обновление профиля пользователя
    profile = Profile.objects.get(user_id=user_id)
    profile.email_verification_code = verification_code
    profile.code_created_at = datetime.now()
    profile.save()
    
    # Отправка email
    subject = 'Подтверждение регистрации'
    message = f'Ваш код подтверждения: {verification_code}\nКод действителен в течение 10 минут.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
@shared_task
def cleanup_expired_codes():
    """Очистка устаревших кодов подтверждения"""
    from .models import Profile
    
    expiration_time = datetime.now() - timedelta(minutes=10)
    Profile.objects.filter(
        email_verified=False,
        code_created_at__lt=expiration_time
    ).update(
        email_verification_code=None,
        code_created_at=None
    )
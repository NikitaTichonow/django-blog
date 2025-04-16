from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from .tasks import send_verification_email
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
        # Отправка кода подтверждения на email
        if instance.email:
            send_verification_email.delay(instance.id, instance.email)


"""
create_user_profile это функция приемника, которая запускается каждый 
раз при создании пользователя. Пользователь является отправителем, 
который несет ответственность за отправку уведомления.

post_save это сигнал, который отправляется в конце метода сохранения.
"""

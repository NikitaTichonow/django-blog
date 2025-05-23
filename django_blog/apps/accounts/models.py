import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from apps.services.utils import unique_slugify
from django.utils import timezone
from django.core.cache import cache


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name="URL", max_length=255, blank=True, unique=True)
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to="images/avatars/%Y/%m/%d/",
        default="images/avatars/default.png",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=("png", "jpg", "jpeg"))],
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name="Информация о себе")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    def is_online(self):
        last_seen = cache.get(f"last-seen-{self.user.id}")
        if last_seen is not None and timezone.now() < last_seen + timedelta(seconds=200):
            return True
        return False

    class Meta:
        """
        Сортировка, название таблицы в базе данных
        """

        ordering = ("user",)
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse("profile_detail", kwargs={"slug": self.slug})

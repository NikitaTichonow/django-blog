import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache
from apps.accounts.models import Profile
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
class TestProfileModel:
    """Этот класс содержит тесты для модели Profile"""

    def setup_method(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = Profile.objects.create(user=self.user, slug="test-slug")

    def test_profile_creation(self):
        """Тестирование создания профиля."""

        assert self.profile.user.username == "testuser"
        assert self.profile.slug == "test-slug"
        assert self.profile.avatar == "images/avatars/default.png"

    def test_is_online(self):
        """Тестирование метода is_online.Имитация того, что пользователь был в сети недавно"""

        cache.set(f"last-seen-{self.user.id}", timezone.now())
        assert self.profile.is_online() is True


@pytest.mark.django_db
class TestUserViews:
    """Тесты для маршрутов, указанных в URL, с использованием Django и pytest.
    Проверяют доступность страниц и функциональность соответствующих представлений."""

    @pytest.fixture
    def create_user(self):
        """Фикстура для создания пользователя и профиля."""
        user = User.objects.create_user(username="testuser", password="password123")
        profile = Profile.objects.create(user=user, slug="testuser-slug")
        return user, profile  # Возвращаем кортеж: (user, profile)

    def test_profile_edit_authenticated(self, client, create_user):
        """Тестирование редактирования профиля для аутентифицированного пользователя."""
        user, profile = create_user  # Извлекаем пользователя и профиль из фикстуры
        client.login(username="testuser", password="password123")
        response = client.get(reverse("accounts:profile_edit"))
        assert response.status_code == status.HTTP_200_OK

    def test_profile_edit_unauthenticated(self, client):
        """Тестирование редактирования профиля для неаутентифицированного пользователя."""
        response = client.get(reverse("accounts:profile_edit"))
        assert response.status_code == status.HTTP_302_FOUND

    def test_profile_detail(self, client, create_user):
        """Тестирование отображения профиля пользователя."""
        user, profile = create_user  # Извлекаем пользователя и профиль
        client.login(username="testuser", password="password123")
        response = client.get(reverse("accounts:profile_detail", kwargs={"slug": profile.slug}))  # Используем slug профиля
        assert response.status_code == status.HTTP_200_OK

    def test_user_register(self, client):
        """Тестирование регистрации нового пользователя."""
        response = client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "password1": "password123",
                "password2": "password123",
            },
        )
        assert response.status_code == status.HTTP_302_FOUND
        assert User.objects.filter(username="newuser").exists()

    def test_user_login(self, client, create_user):
        """Тестирование входа пользователя."""
        user, profile = create_user  # Извлекаем пользователя и профиль
        response = client.post(reverse("accounts:login"), {"username": user.username, "password": "password123"})
        assert response.status_code == status.HTTP_302_FOUND

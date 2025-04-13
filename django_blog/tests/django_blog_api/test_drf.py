import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from apps.blog.models import Category
from django.contrib.auth.models import User
from apps.django_blog_api.serializers import PostSerializer, ProfileSerializer
from rest_framework import status



@pytest.mark.django_db
class TestPostSerializer:
    """Эти тесты проверяют валидные и невалидные данные для обоих сериализаторов"""

    def test_vaid_post_serializer(self):
        author = User.objects.create(username="author", email="author@example.com", password="password123")
        category = Category.objects.create(title="Test Category")
        data = {
            "author": author.id,
            "category": category.id,
            "title": "Test Title",
            "description": "Test Description",
            "text": "Test text content",
        }
        serializer = PostSerializer(data=data)
        assert serializer.is_valid(), f"Ошибки валидации: {serializer.errors}"
        assert serializer.validated_data['title'] == 'Test Title'


    def test_invalid_profile_serializer(self):
        data = {
            "username": "",
            "email": "not-an-email",
        }
        serializer = ProfileSerializer(data=data)
        assert not serializer.is_valid()
        assert "username" in serializer.errors
        assert "email" in serializer.errors


@pytest.mark.django_db
def test_schema_view(client):
    response = client.get(reverse("schema"))
    assert response.status_code == status.HTTP_200_OK
    assert 'application/vnd.oai.openapi' in response["Content-Type"]

@pytest.mark.django_db
def test_redoc_view(client):
    response = client.get(reverse("redoc"))
    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]

@pytest.mark.django_db
def test_swagger_ui_view(client):
    response = client.get(reverse("swagger-ui"))
    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]
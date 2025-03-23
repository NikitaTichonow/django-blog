from rest_framework import serializers
from apps.blog.models import Post
from apps.accounts.models import Profile
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "author",
            "category",
            "title",
            "description",
            "text",
            "thumbnail",
            "create",
        )
        model = Post


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_staff",
            "is_active",
            "date_joined",
        )
        model = User

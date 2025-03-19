from rest_framework import serializers
from apps.blog.models import Post


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

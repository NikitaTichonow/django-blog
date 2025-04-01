from celery import shared_task
from .models import Post
from django.utils import timezone

@shared_task
def publish_post(post_id):
    """
    Задача для публикации поста по его ID.
    """
    try:
        post = Post.objects.get(id=post_id)
        post.status = 'published'
        post.save()
        return f'Пост "{post.title}" опубликован.'
    except Post.DoesNotExist:
        return f'Пост с ID {post_id} не найден.'

@shared_task
def draft_post(post_id):
    """
    Задача для перевода поста в черновик по его ID.
    """
    try:
        post = Post.objects.get(id=post_id)
        post.status = 'draft'
        post.save()
        return f'Пост "{post.title}" переведен в черновик.'
    except Post.DoesNotExist:
        return f'Пост с ID {post_id} не найден.'

@shared_task
def update_post(post_id, title=None, description=None, text=None):
    """
    Задача для обновления поста по его ID.
    """
    try:
        post = Post.objects.get(id=post_id)
        if title:
            post.title = title
        if description:
            post.description = description
        if text:
            post.text = text
        post.update = timezone.now()  # Обновляем время последнего изменения
        post.save()
        return f'Пост "{post.title}" обновлен.'
    except Post.DoesNotExist:
        return f'Пост с ID {post_id} не найден.'

@shared_task
def delete_post(post_id):
    """
    Задача для удаления поста по его ID.
    """
    try:
        post = Post.objects.get(id=post_id)
        post.delete()
        return f'Пост "{post.title}" удален.'
    except Post.DoesNotExist:
        return f'Пост с ID {post_id} не найден.'

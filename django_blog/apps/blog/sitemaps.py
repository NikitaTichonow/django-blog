from django.contrib.sitemaps import Sitemap
from apps.blog.models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        # Получаем все опубликованные посты
        return Post.objects.filter(status="published")

    def lastmod(self, obj):
        return obj.update  # Возвращаем дату последнего обновления

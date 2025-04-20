from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from apps.blog.sitemaps import PostSitemap
from apps.blog.feeds import LatestPostFeed
from django.conf.urls.i18n import i18n_patterns


handler403 = "apps.blog.views.tr_handler403"
handler404 = "apps.blog.views.tr_handler404"
handler500 = "apps.blog.views.tr_handler500"


sitemaps = {
    "posts": PostSitemap,
}

"""
Непереводимые стандартные шаблоны URL-адресов и шаблоны можно 
комбинировать в рамках i18n_patterns, 
чтобы некоторые шаблоны содержали языковой префикс, а другие – нет.
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("api/", include("apps.django_blog_api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("django-ckeditor-5/", include('django_ckeditor_5.urls')),
    path("feeds/latest/", LatestPostFeed(), name="latest_post_feed"),
    path('', include('django_prometheus.urls')),
]

urlpatterns += i18n_patterns(
    path("", include("apps.blog.urls")),
    path("", include("apps.accounts.urls", namespace='accounts')),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls", namespace='djdt'))]

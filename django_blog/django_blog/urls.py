from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from apps.blog.sitemaps import PostSitemap
from apps.blog.feeds import LatestPostFeed


handler403 = "apps.blog.views.tr_handler403"
handler404 = "apps.blog.views.tr_handler404"
handler500 = "apps.blog.views.tr_handler500"


sitemaps = {
    "posts": PostSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path("api/", include("apps.django_blog_api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("apps.blog.urls")),
    path("", include("apps.accounts.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("feeds/latest/", LatestPostFeed(), name="latest_post_feed"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

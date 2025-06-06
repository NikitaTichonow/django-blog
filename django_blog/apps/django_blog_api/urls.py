from django.urls import path
from .views import PostList, PostDetail, ProfileList, ProfileDetail
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("post_list/", PostList.as_view(), name="post_list"),
    path("profile/<int:pk>/", ProfileDetail.as_view(), name="profile_detail"),
    path("profile_list/", ProfileList.as_view(), name="profile_list"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

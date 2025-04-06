from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostFromCategory,
    PostCreateView,
    PostUpdateView,
    CommentCreateView,
    PostByTagListView,
    RatingCreateView,
    PostDeleteView,
    PostSearchView
)
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path(_("post/create/"), PostCreateView.as_view(), name="post_create"),
    path(_("post/<str:slug>/update/"), PostUpdateView.as_view(), name="post_update"),
    path(_("post/<str:slug>/delete/"), PostDeleteView.as_view(), name="post_delete"),
    path(_("post/<str:slug>/"), PostDetailView.as_view(), name="post_detail"),
    path(_("category/<str:slug>/"), PostFromCategory.as_view(), name="post_by_category"),
    path(_("post/<int:pk>/comments/create/"), CommentCreateView.as_view(), name="comment_create_view"),
    path(_("post/tags/<str:tag>/"), PostByTagListView.as_view(), name="post_by_tags"),
    path(_("rating/"), RatingCreateView.as_view(), name="rating"),
    path(_('post_search/'), PostSearchView.as_view(), name='post_search'),
]

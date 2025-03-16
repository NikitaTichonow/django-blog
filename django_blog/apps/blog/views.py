from django.views.generic import ListView, DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class PostDetailView(DetailView):
    model = Post  # model - название нашей модели, Post.
    template_name = "blog/post_detail.html"  # template_name - По умолчанию DetailView ищет шаблон с префиксом имени модели и суффиксом _detail.html
    context_object_name = "post"  #  context_object_name - переопределим имя Queryset по умолчанию

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context

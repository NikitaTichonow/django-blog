from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 4
    queryset = Post.custom.all()

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


class PostFromCategory(ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    category = None
    paginate_by = 1

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs["slug"])
        queryset = Post.objects.filter(category__slug=self.category.slug)
        if not queryset:
            sub_cat = Category.objects.filter(parent=self.category)
            queryset = Post.objects.filter(category__in=sub_cat)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Записи из категории: {self.category.title}"
        return context

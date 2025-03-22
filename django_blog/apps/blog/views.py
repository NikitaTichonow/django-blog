from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Category
from .forms import PostCreateForm, PostUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.http import JsonResponse
from django.shortcuts import redirect
from .forms import CommentCreateForm
from .models import Comment

from ..services.mixins import AuthorRequiredMixin


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
        context["form"] = CommentCreateForm
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """

    model = Post
    template_name = "blog/post_create.html"
    form_class = PostCreateForm
    login_url = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавление статьи на сайт"
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """

    model = Post
    template_name = "blog/post_update.html"
    context_object_name = "post"
    form_class = PostUpdateForm
    login_url = "home"
    success_message = "Запись была успешно обновлена!"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление статьи: {self.object.title}"
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def is_ajax(self):
        return self.request.headers.get("X-Requested-With") == "XMLHttpRequest"

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({"error": form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get("pk")
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get("parent")
        comment.save()

        if self.is_ajax():
            return JsonResponse(
                {
                    "is_child": comment.is_child_node(),
                    "id": comment.id,
                    "author": comment.author.username,
                    "parent_id": comment.parent_id,
                    "time_create": comment.time_create.strftime("%Y-%b-%d %H:%M:%S"),
                    "avatar": comment.author.profile.avatar.url,
                    "content": comment.content,
                    "get_absolute_url": comment.author.profile.get_absolute_url(),
                },
                status=200,
            )

        return redirect(comment.post.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({"error": "Необходимо авторизоваться для добавления комментариев"}, status=400)

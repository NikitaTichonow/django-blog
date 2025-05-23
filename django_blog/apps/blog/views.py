from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View, DeleteView
from .models import Post, Category, Comment, Rating
from .forms import PostCreateForm, PostUpdateForm, SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.http import JsonResponse
from django.shortcuts import redirect
from .forms import CommentCreateForm

from django.shortcuts import render

from django.contrib.postgres.search import SearchVector
from taggit.models import Tag

from ..services.mixins import AuthorRequiredMixin


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(
        request=request,
        template_name="errors/error_page.html",
        status=404,
        context={
            "title": "Страница не найдена: 404",
            "error_message": "К сожалению такая страница была не найдена, или перемещена",
        },
    )


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(
        request=request,
        template_name="errors/error_page.html",
        status=500,
        context={
            "title": "Ошибка сервера: 500",
            "error_message": "Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта",
        },
    )


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(
        request=request,
        template_name="errors/error_page.html",
        status=403,
        context={
            "title": "Ошибка доступа: 403",
            "error_message": "Доступ к этой странице ограничен",
        },
    )


class PostSearchView(View):
    def get(self, request):
        form = SearchForm()
        query = request.GET.get("query")
        results = []

        if query:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data["query"]
                results = Post.objects.annotate(search=SearchVector("title", "description")).filter(search=query)

        return render(request, "blog/post_search.html", {"form": form, "query": query, "results": results})


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


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """

    permission_required = "blog.add_post"
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


class PostDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: удаления материала на сайте
    """

    model = Post
    template_name = "blog/post_confirm_delete.html"
    context_object_name = "post"
    success_message = "Запись успешно удалена"
    success_url = reverse_lazy("home")

    def get_queryset(self):
        # Ограничиваем доступ к удалению только автору поста
        return self.model.objects.filter(author=self.request.user)


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


class PostByTagListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs["tag"])
        queryset = Post.objects.filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Статьи по тегу: {self.tag.name}"
        return context


class RatingCreateView(View):
    model = Rating

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get("post_id")
        value = int(request.POST.get("value"))
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded_for.split(",")[0] if x_forwarded_for else request.META.get("REMOTE_ADDR")
        ip_address = ip
        user = request.user if request.user.is_authenticated else None

        rating, created = self.model.objects.get_or_create(
            post_id=post_id,
            ip_address=ip_address,
            defaults={"value": value, "user": user},
        )

        if not created:
            if rating.value == value:
                rating.delete()
                return JsonResponse({"status": "deleted", "rating_sum": rating.post.get_sum_rating()})
            else:
                rating.value = value
                rating.user = user
                rating.save()
                return JsonResponse({"status": "updated", "rating_sum": rating.post.get_sum_rating()})
        return JsonResponse({"status": "created", "rating_sum": rating.post.get_sum_rating()})

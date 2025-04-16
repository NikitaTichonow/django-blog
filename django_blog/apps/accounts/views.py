from django.views.generic import DetailView, UpdateView, CreateView, View
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm, UserRegisterForm, UserLoginForm


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """

    model = Profile
    context_object_name = "profile"
    template_name = "accounts/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Профиль пользователя: {self.object.user.username}"
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """

    model = Profile
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_edit.html"

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"Редактирование профиля пользователя: {self.request.user.username}"
        if self.request.POST:
            context["user_form"] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context["user_form"] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context["user_form"]
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({"user_form": user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("accounts:profile_detail", kwargs={"slug": self.object.slug})


class UserRegisterView(SuccessMessageMixin, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """

    form_class = UserRegisterForm
    success_url = reverse_lazy("accounts:verify_email")
    template_name = "accounts/user_register.html"
    success_message = "Вы успешно зарегистрировались. Пожалуйста, подтвердите ваш email."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """

    form_class = UserLoginForm
    template_name = "accounts/user_login.html"
    next_page = "home"
    success_message = "Добро пожаловать на сайт!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация на сайте"
        return context


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """

    next_page = "home"


class VerifyEmailView(View):
    """
    Представление для подтверждения email
    """
    template_name = 'accounts/verify_email.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = request.POST.get('verification_code')
        profile = request.user.profile

        if not profile.email_verification_code or not profile.code_created_at:
            messages.error(request, 'Код подтверждения не найден или устарел. Пожалуйста, запросите новый код.')
            return render(request, self.template_name, {'error_message': 'Код подтверждения не найден'})

        # Проверка срока действия кода (10 минут)
        if timezone.now() - profile.code_created_at > timedelta(minutes=10):
            profile.email_verification_code = None
            profile.code_created_at = None
            profile.save()
            messages.error(request, 'Срок действия кода истек. Пожалуйста, запросите новый код.')
            return render(request, self.template_name, {'error_message': 'Срок действия кода истек'})

        if code == profile.email_verification_code:
            profile.email_verified = True
            profile.email_verification_code = None
            profile.code_created_at = None
            profile.save()
            messages.success(request, 'Email успешно подтвержден!')
            return redirect('home')
        else:
            messages.error(request, 'Неверный код подтверждения')
            return render(request, self.template_name, {'error_message': 'Неверный код подтверждения'})

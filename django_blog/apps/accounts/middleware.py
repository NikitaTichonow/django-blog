from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Логика обработки запроса
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f"last-seen-{request.user.id}"
            last_login = cache.get(cache_key)
            print(last_login)
            if not last_login:
                User.objects.filter(id=request.user.id).update(last_login=timezone.now())
                # Устанавливаем кэширование на 300 секунд с текущей датой по ключу last-seen-id-пользователя
                cache.set(cache_key, timezone.now(), 300)

        # Передача управления следующему middleware или view
        response = self.get_response(request)
        return response

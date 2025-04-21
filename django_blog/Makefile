VENV_PATH = ..\venv\Scripts\activate
PROJECT_DIR = django_blog

PROMETHEUS_PATH = C:\Program Files\Prometheus\prometheus.exe
# Команды
.PHONY: help run migrate makemigrations collectstatic shell test  celery celery-worker celery-beat celery-flower redis

help:  ## Показать доступные команды
	@echo "Доступные команды:"
	@echo "  make run            - Запустить сервер разработки"
	@echo "  make migrate        - Применить миграции"
	@echo "  make makemigrations - Создать миграции"
	@echo "  make collectstatic  - Собрать статические файлы"
	@echo "  make shell          - Запустить оболочку Django"
	@echo "  make test           - Запустить тесты pytest"
	@echo "  make black          - Запустить black(форматировщик кода на Python)"
	@echo "  make dumpdata       - Запустить dumpdata(Выгрузка существующих данных в mysite_data.json)"
	@echo "  make loaddata       - Запустить loaddata(Загрузка существующих данных из mysite_data.json)"

run:  ## Запустить сервер разработки
	python manage.py runserver

migrate:  ## Применить миграции
	python manage.py migrate

makemigrations:  ## Создать миграции
	python manage.py makemigrations

collectstatic:  ## Собрать статические файлы
	python manage.py collectstatic --noinput

shell:  ## Запустить оболочку Django
	python manage.py shell

test:  ## Запустить тесты pytest
	pytest

black: ## 
	black . --exclude=venv

dumpdata: ## 
	python -Xutf8 manage.py dumpdata --exclude contenttypes --indent=2 --output=mysite_data.json

loaddata: ##
	python -Xutf8 manage.py loaddata mysite_data.json

prometheus:  ## Запустить Prometheus сервер
	"$(PROMETHEUS_PATH)" --config.file="..\prometheus.yml"

redis:
	cmd /c "redis-server"

celery-worker:
	cmd /c "$(VENV_PATH) && celery -A django_blog worker -l info --pool=solo"

celery-beat:
	cmd /c "$(VENV_PATH) && celery -A django_blog beat -l info"

celery-flower:
	cmd /c "$(VENV_PATH) && celery -A django_blog flower"

celery:
	cmd /c "$(VENV_PATH) && start cmd /c redis-server"
	timeout /t 5
	cmd /c "$(VENV_PATH) && start cmd /c celery -A django_blog worker -l info --pool=solo"
	timeout /t 2
	cmd /c "$(VENV_PATH) && start cmd /c celery -A django_blog beat -l info"
	timeout /t 2
	cmd /c "$(VENV_PATH) && start cmd /c celery -A django_blog flower"
	cmd /c "$(VENV_PATH) && start cmd /c python manage.py runserver 8001 --noreload

sentry-test:
	python manage.py shell -c "raise Exception('Test Sentry Integration')"

# # Укажите имя вашего виртуального окружения
# VENV_NAME=venv

# Укажите имя вашего проекта
PROJECT_NAME=django_blog

# # Укажите команду для активации виртуального окружения
# ACTIVATE= $(VENV_NAME)/bin/activate

# # Команды
# # Укажите имя вашего виртуального окружения
# VENV_NAME=venv

# # Укажите команду для активации виртуального окружения
# ACTIVATE=  venv\Scripts\activate 

# Команды
.PHONY: help run migrate makemigrations collectstatic shell test

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
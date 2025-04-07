<h1 align="center">Django_Blog Project</h1>
Этот проект представляет собой Django_Blog на python, django, которое позволяет пользователям  регистрироваться на портале, просматривать записи, коментировать. Администраторам портала доступно создание записей, редактирование(своих записей) Приложение использует DRF. Реализована система смены языка. 

<h2 align="center">Установка</h2>

1. **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/NikitaTichonow/django-blog

2. **Перейдите в папку проекта:**
    ```bash
    cd django-blog

3. **Установите необходимые зависимости:**
     ```bash
    pip install -r requirements.txt    
   
5. **Откройте файл .env.template и заполнить его своими данными**
   ```env
    SECRET_KEY_ENV="................."

6. **Запустите сервер разработки:**
    ```bash
    python manage.py runserver
    
    
7. **Доступ к приложению:**
    ```После завершения всех вышеуказанных шагов, приложение будет доступно по адресу 
    http://127.0.0.1:8000

    
7. **Доступ к документации Django Rest Framework:**
    ```Schema Django Rest Framework 
    'http://127.0.0.1:8000/api/profile_list/'   Список всех пользователей(доступный администраторам)

    'http://127.0.0.1:8000/api/post_list/' Список всех записей(доступный администраторам)

    ```Schema redoc 
    http://127.0.0.1:8000/api/schema/redoc/ 

    ```Schema swagger-ui 
    http://127.0.0.1:8000/api/schema/swagger-ui/ 

<p align="center">
  <img src="" width="350">
  <img src="" width="350">
</p>

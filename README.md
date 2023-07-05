# FOODGRAM

FOODGRAM это удобный сайт для размещения и поиска рецептов.

### Технологии:

Python, Django, Docker, Gunicorn, NGINX, PostgreSQL, Yandex Cloud.

### Для запуска проект необходимо:

- Клонировать репозиторий:d
```
https://github.com/nemanick/foodgram-project-react.git
```
- В директории проекта создать виртуальное окружение и установить sdзависимости:
```
python -m venv venv
```
```
pip install -r requirements.txt
```

- Выполнить миграции:
```
python backends/manage.py migrate
```

### Работа с api
- В проекте уже создана админка, несколько рецептов и юзеров, а также в базу были добавлены ингредиенты для более удобной работы.

- Админка доступна по ссылке [http://127.0.0.1:8000/admin/].

```
admin:
email: admin@admin.com
password: admin
```
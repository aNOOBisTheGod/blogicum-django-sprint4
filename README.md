# Блогикум: часть 3

Django-приложение с публикациями, профилями пользователей и комментариями.

## Запуск

Требуется Python 3.12.

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd blogicum
python manage.py migrate
python manage.py loaddata ../db.json
python manage.py createsuperuser
python manage.py runserver
```

Из корня репозитория: `pytest` и `flake8 blogicum`.

Автор может создавать, редактировать и удалять свои посты и комментарии.
Отложенные и снятые с публикации записи доступны только автору.
Списки содержат по 10 записей на странице; изображения хранятся локально.
Почта сохраняется в `blogicum/sent_emails/`.

SECRET_KEY в настройках предназначен для учебной локальной разработки.

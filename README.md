# Проект: social_blog_fastapi

---

### Стек:
Python, FastApi, PostgreSql, SqlAlchemy, Pydantic, fastapi-pagination

---

### Описание:

**social_blog_fastapi** - это API написанная на FastApi для social_blog(https://github.com/CHEDEIV8/social_blog). Позволяющая просматривать и создавать посты, просматривать группы, подписываться на авторов постов.

---

### Как развернуть проект:

1. Клонировать репозиторий:

```
	git@github.com:CHEDEIV8/social_blog_fastapi.git
```

2. Создать в папке app/ файл **.env** с переменными окружения (см. [.env.example](.env.example)).

3. Cоздать и активировать виртуальное окружение::
```
	python -m venv venv
    source venv/Scripts/activate
```

4. Обновляем версию pip:

```
    python -m pip install --upgrade pip
```

5. Установить зависимости из файла requirements.txt:

```
    pip install -r requirements.txt
```

6. Запустить проект:

```
    uvicorn app.main:app
```

---

### Примеры запросов к API:

1. Создать пользователя (POST):
http://127.0.0.1:8000/api/v1/users/

2. Получить токен (POST):
http://127.0.0.1:8000/api/v1/jwt/create/

3. Получить список всех постов (GET):
http://127.0.0.1:8000/api/v1/posts/

4. Получить определенный пост (GET):
http://127.0.0.1:8000/api/v1/posts/1/

5. Получить коментарии определенного поста (GET):
http://127.0.0.1:8000/api/v1/posts/1/comments/

6. Получить список всех групп (GET):
http://127.0.0.1:8000/api/v1/groups/

7. Создать новый пост(требуется аутентификация) (POST):
http://127.0.0.1:8000/api/v1/posts/

8. Получить документацию по всем эндпойнтам API (GET):
http://127.0.0.1:8000/docs/


### Об авторе

Автор проекта: **Денис Чередниченко**
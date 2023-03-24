# Проект YaMDb - сервис отзывов на произведения

### Авторы:
- [Анастасия Стёпина](https://github.com/KDeviant66 "Github page")
- [Александр Горленко](https://github.com/agorlenko2 "Github page")
- [Николай Дубинин](https://github.com/nikdubinin "Github page")

### Технологии:
- Python 3.9.10
- Django 3.2
- Django REST framework 3.12.4
- Simple JWT - 4.8.0

### 
Сервис собирает отзывы на произведения различных категорий (например: книги, песни, фильмы). Произведению может быть присвоен жанр. Каждое произведение получает рейтинг на основе оценок пользователей (от 1 до 10).

С помощью этого проекта можно:
* Читать отзывы на произведения различных категорий и жанров, а также ставить им оценки
* Добавлять, изменять и удалять собственные отзывы
* Оставлять комментарии к отзывам

#### Документация:
```
http://localhost:8000/redoc/
```
### Запуск проекта:

Клонируем репозиторий и перейти в него в терминале:

```
git clone https://github.com/nikdubinin/api_yamdb.git
```

```
cd api_yamdb
```

Cоздаем и активируем виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установливаем зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создаем миграции:

```
python manage.py makemigrations reviews
```

Выполняем миграции:

```
python3 manage.py migrate
```

Заполняем базу данных тестовой информацией:

```
python manage.py csv_to_db
```

Запуск проекта:

```
python3 manage.py runserver
```

## Примеры запросов

* ### Регистрация нового пользователя
    **Request**
    ```
        POST /api/v1/auth/signup/
        body: {"email": "string", "username": "string"}
    ```
    **Response**
    ```
        {
          "email": "string",
          "username": "string",
        }
    ```

* ### Получить JWT-токен
    **Request**
    ```
        POST /api/v1/auth/token/
        body: {"username": "string", "confirmation_code": "string"}
    ```
    **Response**
    ```
        {
          "token": "string",
        }
    ```

* ### Получение списка всех категорий
    **Request**
    ```
        GET /api/v1/categories/
    ```
    **Response**
    ```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
            "name": "string",
            "slug": "string"
            }
        ]
    }
  ```

* ### Добавление новой категории
    **Request**
    ```
        POST /api/v1/categories/
        body: {"name": "string", "slug": "string"}
    ```
    **Response**
    ```
        {
            "name": "string",
            "slug": "string"
        }
    ```

* ### Удаление категории
    **Request**
    ```
        DELETE /api/v1/categories/{slug}/
    ```
    **Response**
    ```
        status_code: 204
    ```

* ### Получение списка всех жанров
    **Request**
    ```
        GET /api/v1/genres/
    ```
    **Response**
    ```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
  ```

* ### Добавление жанра
    **Request**
    ```
        POST /api/v1/genres/
        body: {"name": "string", "slug": "string"}
    ```
    **Response**
    ```
        {
            "name": "string",
            "slug": "string"
        }
    ```

* ### Удаление жанра
    **Request**
    ```
        DELETE /api/v1/genres/{slug}/
    ```
    **Response**
    ```
        status_code: 204
    ```

* ### Получение списка всех произведений
    **Request**
    ```
        GET /api/v1/titles/
    ```
    **Response**
    ```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
            "id": 0,
            "name": "string",
            "year": 0,
            "rating": 0,
            "description": "string",
            "genre": [
                {
                    "name": "string",
                    "slug": "string"
                }
            ],
            "category": {
                "name": "string",
                "slug": "string"
                }
            }
        ]
    }
  ```

* ### Добавление произведения
    **Request**
    ```
        POST /api/v1/titles/
        body: {"name": "string", "year": 0, "description": "string", "genre": ["string"], "category": "string"}
    ```
    **Response**
    ```
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
                "name": "string",
                "slug": "string"
            }
        ],
        "category": {
            "name": "string",
            "slug": "string"
        }
    }
    ```

* ### Получение информации о произведении по его id
    **Request**
    ```
        GET /api/v1/titles/{title_id}/
    ```
    **Response**
    ```
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
                "name": "string",
                "slug": "string"
            }
        ],
        "category": {
            "name": "string",
            "slug": "string"
        }
    }
    ```

* ### Частичное обновление информации о произведении по его id
    **Request**
    ```
        PATCH /api/v1/titles/{title_id}/
        body: {"name": "string", "year": 0, "description": "string", "genre": ["string"], "category": "string"}
    ```
    **Response**
    ```
    {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
            {
                "name": "string",
                "slug": "string"
            }
        ],
        "category": {
            "name": "string",
            "slug": "string"
            }
    }
   ```

* ### Удаление публикации по её id
    **Request**
    ```
        DELETE /api/v1/titles/{title_id}/
    ```
    **Response**
    ```
        status_code: 204
    ```

* ### Получение списка всех отзывов
    **Request**
    ```
        GET /api/v1/titles/{title_id}/reviews/
    ```
    **Response**
    ```
        {
            "count": 0,
            "next": "string",
            "previous": "string",
            "results": [
                {
                    "id": 0,
                    "text": "string",
                    "author": "string",
                    "score": 1,
                    "pub_date": "2019-08-24T14:15:22Z",
 
                }
            ]
        }
    ```

* ### Добавление нового отзыва
    **Request**
    ```
        POST /api/v1/titles/{title_id}/reviews/
        body: {"text": "string", "score": 1}
    ```
    **Response**
    ```
            {
                "id": 0,
                "text": "string",
                "author": "string",  
                "score": 1,
                "pub_date": "2019-08-24T14:15:22Z"
            }
    ```

* ### Полуение отзыва по id
    **Request**
    ```
        GET /api/v1/titles/{title_id}/reviews/{review_id}/
    ```
    **Response**
    ```
            {
                "id": 0,
                "text": "string",
                "author": "string",  
                "score": 1,
                "pub_date": "2019-08-24T14:15:22Z"
            }
    ```

* ### Частичное обновление отзыва по id
    **Request**
    ```
        PATCH /api/v1/titles/{title_id}/reviews/{review_id}/
        body: {"text": "string", "score": 1}
    ```
    **Response**
    ```
            {
                "id": 0,
                "text": "string",
                "author": "string",  
                "score": 1,
                "pub_date": "2019-08-24T14:15:22Z"
            }
    ```

* ### Удаление отзыва по id
    **Request**
    ```
        DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
    ```
    **Response**
    ```
        status_code: 204
    ```

* ### Получение списка всех комментариев к отзыву
    **Request**
    ```
        GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
    ```
    **Response**
    ```
        {
            "count": 0,
            "next": "string",
            "previous": "string",
            "results": [
                {
                    "id": 0,
                    "text": "string",
                    "author": "string",
                    "pub_date": "2019-08-24T14:15:22Z",
 
                }
            ]
        }
    ```


* ### Добавление комментария к отзыву
    **Request**
    ```
        POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
        body: {"text": "string"}
    ```
    **Response**
    ```
            {
                "id": 0,
                "text": "string",
                "author": "string",
                "pub_date": "2019-08-24T14:15:22Z",
            }
    ```

* ### Получение комментария к отзыву
    **Request**
    ```
        GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    ```
    **Response**
    ```
            {
                "id": 0,
                "text": "string",
                "author": "string",  
                "pub_date": "2019-08-24T14:15:22Z"
            }
    ```

* ### Частичное обновление комментария к отзыву
    **Request**
    ```
        PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
        body: {"text: "string"}
    ```
    **Response**
    ```
            {
                "id": 0,
                "text": "string",
                "author": "string",  
                "pub_date": "2019-08-24T14:15:22Z"
            }
    ```

* ### Удаление комментария к отзыву
    **Request**
    ```
        DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
    ```
    **Response**
    ```
        status_code: 204
    ```

* ### Получение списка всех пользователей
    **Request**
    ```
        GET /api/v1/users/
    ```
    **Response**
    ```
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "username": "string",
                "email": "user@example.com",
                "first_name": "string",
                "last_name": "string",
                "bio": "string",
                "role": "user"
            }
        ]
    }
    ```

* ### Добавление пользователя
    **Request**
    ```
        POST /api/v1/users/
        body: {"username": "string", "email": "user@example.com", "first_name": "string", "last_name": "string", "bio": "string", "role": "user"}
    ```
    **Response**
    ```
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ```

* ### Получение пользователя по username
    **Request**
    ```
        GET /api/v1/users/{username}/
    ```
    **Response**
    ```
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ```

* ### Изменение данных пользователя по username
    **Request**
    ```
        PATCH /api/v1/users/{username}/
        body: {"username": "string", "email": "user@example.com", "first_name": "string", "last_name": "string", "bio": "string", "role": "user"}
    ```
    **Response**
    ```
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ```

* ### Удаление пользователя по username
    **Request**
    ```
        DELETE /api/v1/users/{username}/
    ```
    **Response**
    ```
        status_code: 204
    ```

* ### Получение данных своей учетной записи
    **Request**
    ```
        GET /api/v1/users/me/
    ```
    **Response**
    ```
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ```

* ### Изменение данных своей учетной записи
    **Request**
    ```
        PATCH /api/v1/users/me/
        body: {"username": "string", "email": "user@example.com", "first_name": "string", "last_name": "string", "bio": "string"}
    ```
    **Response**
    ```
        {
            "username": "string",
            "email": "user@example.com",
            "first_name": "string",
            "last_name": "string",
            "bio": "string",
            "role": "user"
        }
    ```
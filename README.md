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

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/nikdubinin/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать миграции:

```
python manage.py makemigrations reviews
```

Выполнить миграции:

```
python3 manage.py migrate
```

Заполнить базу данных тестовой информацией:

```
python manage.py csv_to_db
```

Запустить проект:

```
python3 manage.py runserver
```

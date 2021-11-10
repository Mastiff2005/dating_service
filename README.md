# Dating service
API для сайта (приложения) знакомств, парсер товаров. Тестовое задание.
### Технологии:
* Python 3.9
* Django
* Django REST framework
* Docker
* Celery
* Redis

### Запуск проекта

Для запуска должны быть установлены Docker и docker-compose

*  #### Клонируйте репозиторий командой:

git clone https://github.com/Mastiff2005/dating_service.git

* #### Перейдите в директорию командой:

cd dating_service

* #### Переименуйте файл .env.exapmle в .env:

mv .env.example .env

* #### Выполните команду для запуска контейнера:

docker-compose up -d

* ####  Выполните миграции:

docker-compose exec web python manage.py makemigrations --noinput
docker-compose exec web python manage.py migrate --noinput

* #### Команда для сбора статики:

docker-compose exec web python manage.py collectstatic --no-input

* #### Команда для создания суперпользователя:

docker-compose exec web python manage.py createsuperuser
***

Документация по API будет доступна по адресам http://127.0.0.1/swagger/ , http://127.0.0.1/redoc/

При открытии главной страницы http://127.0.0.1 с помощью Celery запускается парсер товаров, товары сохраняются в базу данных.

Список товаров доступен по эндпойнту http://127.0.0.1/api/products

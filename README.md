![Yamdb workflow](https://github.com/Glaser1/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)


# Yamdb 
## Описание

Yamdb предоставляет API для доступа к базе данных произведений искусства и отзывов к ним и позволяет:
* просматривать категории и жанры произведений искусства
* просматривать и создавать отзывы к произведениям 
* оставлять комментарии к отзывам
* пользователи с правами администратора может создавать и обновлять категории и жанры

## Шаблон наполнения env-файла:
``` DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql ```

``` DB_NAME=postgres # имя базы данных ```

``` POSTGRES_USER=postgres # логин для подключения к базе данных ```

``` POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой) ```

``` DB_HOST=db # название сервиса (контейнера) ```

``` DB_PORT=5432 # порт для подключения к БД ```

## Установка:
* Клонируйте репозиторий себе на компьютер;
* Перейдите в рабочую папку: cd infra_sp2;
* Запустите приложения в контейнерах: docker-compose up -d
* Выполните миграцию в контейнерах: 

  ``` docker-compose web bash ```

  ``` docker-compose exec web python manage.py makemigrations reviews ```
  
  ``` docker-compose exec web python manage.py migrate ```

* Соберите статические файлы:
  ``` docker-compose exec web python manage.py collectstatic --no-input ```
* Создайте суперпользователя:
  ``` docker-compose exec web python manage.py createsuperuser ```

## Примеры запросов к API:
 - Получить список всех произведений (GET-запрос):
   ``` /api/v1/titles/ ```
 - Получить список всех отзывов на произведение (GET-запрос):
   ``` /api/v1/titles/{title_id}/reviews/ ```
 - Получить список всех комментариев к отзыву (GET-запрос):
   ``` /api/v1/titles/{title_id}/reviews/{review_id}/comments/ ```
 - Получение списка всех жанров (GET-запрос):
  ``` /api/v1/genres/ ```
 - Добавление нового отзыва (POST-запрос):
  ``` /api/v1/titles/{title_id}/reviews/ ```
  
  ## Документация:
Доступна будет доступна после запуска по адресу: (https:<ip_адрес_вашего_сервера>/redoc/)


## Авторы проекта:
  Виталий Усенко: https://github.com/vitalyuvv

  Юрий Ребрик: https://github.com/gkirber

  Александр Плисков: https://github.com/Glaser1


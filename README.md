# FoodGram продуктовый помощник
![Yamdb Workflow Status](https://github.com/splintermax/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg?branch=master&event=push)

## Описание проекта Foodgram
«Продуктовый помощник»: приложение, в котором пользователи могут:
1. Публиковать рецепты;
2. Подписываться на публикации других авторов;
3. Добавлять рецепты в избранное;
4. Загрузить список покупок из выбранных рецептов.

Посмотреть проект можно [тут](http://korkin.ddns.net)

Суперпользователь:

Логин: splintermax92@yandex.ru
Пароль: KmO13051992



## Запуск проекта на удаленном сервере:

- В папке infra выполнить команду, чтобы собрать контейнер:

```
sudo docker-compose up -d
```

Для отображения проекта необходимо выполнить команды:

```
sudo docker-compose exec backend python manage.py migrate
```
```
sudo docker-compose exec backend python manage.py createsuperuser
```
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

Для наполнения базы ингредиентами и тэгами необходимо выполнить команды:

```
sudo docker-compose exec backend python manage.py load_tags
```
```
sudo docker-compose exec backend python manage.py load_ingredients
```

Над проектом работал [Максим Коркин](https://github.com/splintermax)
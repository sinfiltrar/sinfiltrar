# sinfiltrar-api

sinfiltr.ar API - input processing and API

Django based project.

Install
-------

```
$ mkvirtualenv sf
$ pip install -r requirements.txt
$ python manage.py migrate
```

Develop
-------

To run locally:

```
$ python manage.py runserver
```

then visit `http://localhost:8000`

Deployment
----------

Commands:

```
$ zappa deploy dev
$ zappa update dev
$ zappa status dev
$ zappa tail dev
```

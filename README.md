# Challenge Groover

> :warning: This API is in **development stage**.

This project aims to meet [Groover's backend development challenge](https://github.com/Groover-Dev/ChallengeBackend) summerized in `INSTRUCTION.md`.

This project is built with:
* Docker
* Python
* Django and Django REST Framework
* PostgreSQL

## Project setup

Before starting, [install Compose](https://docs.docker.com/compose/install/).

Add your spotify client id and secret key to an `.env` file at the root of the project and also fill in a `DJANGO_SECRET_KEY`.

```
# .env

# Spotify credentials
CLIENT_ID=yourID
CLIENT_SECRET=yourSecret

# Production credentials
DJANGO_SECRET_KEY=yourServerSecretKey
PORT=5000
```

Build database and app containers and run developement server with:

```
$ docker-compose up
```

Then, migrate and create a super user providing 
an email and a username:

```
$ docker-compose exec app python manage.py migrate

$ docker-compose exec app python manage.py createsuperuser --email youremail@example.io --username fooAdmin
```

## Production

For a production purpose, first fill in a `PORT` variable in `.env` file to inform on which port run the Django server. Then use docker commands above together with `prod/production.yml` file with admin's email and username:

```
$ docker-compose -f docker-compose.yml -f prod/production.yml up

$ docker-compose -f docker-compose.yml -f prod/production.yml exec app python manage.py migrate

$ docker-compose -f docker-compose.yml -f prod/production.yml exec app python manage.py createsuperuser --email youremail@example.io --username fooAdmin
```
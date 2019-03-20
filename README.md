# Portal

## Install

```bash
docker-compose up --build
```

## Dev

```bash
# run the Django project and unit tests
docker-compose up

# just run the Django project
docker-compose up portal
```

## Deploy

Deployed to AWS Lambda with [Zappa](https://github.com/Miserlou/Zappa). Read the docs for a list of commands.

Frequent commands listed below, replace `dev` with the appropriate {stage}:

```bash
# activate a virtual env
source env/bin/activate

# first time deploy
zappa deploy dev

# update an existing deploy
zappa update dev

# logs
zappa tail dev

# to apply db migrations
zappa manage dev migrate

# add an admin user, then need to log in and update the details
zappa manage <stage> create_admin_user
```

## Tests

```bash
# Make sure the Docker container is running and in a new Terminal run
docker-compose exec portal /bin/bash

# to run the test suite
python manage.py test

# to run the test suite for an app e.g. {home}
python manage.py test home

# to run coverage report
coverage run --source='.' manage.py test
coverage report
```

## Django Install

**Deprecated**

```bash
# create a virtualenv
virtualenv -p python3 env

# activate the virtualenv
source env/bin/activate

# install requirements
pip install -r requirements-dev.txt

# confirm django is installed, will return the version number from requirements.txt
python -m django --version
```

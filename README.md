# Portal

[![CircleCI](https://circleci.com/gh/sam-atkins/portal/tree/release.svg?style=svg)](https://circleci.com/gh/sam-atkins/portal/tree/release)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Table of Contents

- [Install](#install)
- [Dev](#dev)
- [Tests](#tests)
- [Deploy](#deploy)

## Install

```bash
docker-compose up --build
```

In order to test deployment locally, change the stage in the docker-compose file to a remote stage e.g. `dev`. Docker requires some environment variables. If these are available in your Terminal session it will pick them up, otherwise add them to a `.env` file e.g.

```
AWS_ACCESS_KEY_ID=XXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXX
AWS_REGION=XXXXXXXX
```

## Dev

```bash
# run the Django project and unit tests
docker-compose up

# just run the Django project
docker-compose up portal
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

## Deploy

Deployed to AWS Lambda with [Zappa](https://github.com/Miserlou/Zappa), refer to their docs for a full list of commands.

Frequent commands listed below, replace `dev` with the appropriate {stage}:

```bash
# initialize a Python 3 virtual environment
pipenv --three

# activate pipenv shell
pipenv shell

# Zappa needs the project's requirements to be installed in the virtual env
pipenv install

# first time deploy
zappa deploy dev

# update an existing deploy
zappa update dev

# logs
zappa tail dev

# to apply db migrations
zappa manage dev migrate

# add an admin user, then log in and update the details
zappa manage <stage> create_admin_user
```

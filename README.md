# Portal

[![CircleCI](https://circleci.com/gh/sam-atkins/portal.svg?style=svg)](https://circleci.com/gh/sam-atkins/portal)
<a href="https://github.com/ambv/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Table of Contents

- [Description](#description)
- [Install](#install)
- [Dev](#dev)
- [Tests](#tests)
- [Deploy](#deploy)

## Description

This is a learning project, primarily experimenting with a micro-service Serverless architecture.

The project includes:

- Django web app deployed with Zappa to run on AWS Lambda (this repo)
- `manageconf` [PyPi package](https://pypi.org/project/manageconf/) to manage configuration and service discovery
- [Met service](https://github.com/sam-atkins/met-service) to fetch weather data

## Install

```bash
docker-compose up --build
```

In order to test deployment locally, change the stage in the docker-compose file to a remote stage e.g. `dev`. Docker requires some environment variables. If these are available in your Terminal session it will pick them up, otherwise add them to a `.env` file e.g.

```
AWS_ACCESS_KEY_ID=XXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXX
AWS_REGION=XXXXXXXX
POSTMAN_MOCK_SERVER_API_KEY_MET_SERVICE=XXXXXXXX
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
# initialize a Python 3.6 virtual environment
virtualenv -p python3.6 env

# activate the virtual env
source env/bin/activate

# Zappa needs the project's requirements to be installed in the virtual env
pip install requirements-dev.txt

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

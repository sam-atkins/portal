# Portal

## Install

```bash
docker-compose up --build
```

## Dev

```bash
docker-compose up
```

## Tests

```bash
# Make sure the Docker container is running and in a new Terminal run
docker-compose exec web-portal /bin/bash

# to run the test suite
python manage.py test

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

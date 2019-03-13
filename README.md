# Portal

## Install

```
docker-compose up --build
```

## Dev

```bash
docker-compose up
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

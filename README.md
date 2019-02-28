# Portal

## Install

```bash
# create a virtualenv
virtualenv -p python3 env

# activate the virtualenv
source env/bin/activate

# install requirements
pip install -r requirements.txt

# confirm django is installed, will return the version number from requirements.txt
python -m django --version
```

## Dev

```bash
python manage.py runserver
```

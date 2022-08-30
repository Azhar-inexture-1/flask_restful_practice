# Flask Social Authentication

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/) 

This repository contains the example code for todo app containing social authentication and celery.

## Setup

### Clone this repository.
### Create a virtualenv and install the requirements
```commandline
python3 -m virtualenv myvenv
pip install -r requirements.txt
```

### Add Configuration in core.config file

Create a .env file and add your credentials, the file will automatically
be loaded and configuration
will be added in the config file.
```commandline
# .env

username=''
password=''
database=''
port=5432
host=localhost
SECRET_KEY='your secret key'
GOOGLE_CLIENT_ID=''
GOOGLE_CLIENT_SECRET=''
TWITTER_CLIENT_ID=''
TWITTER_CLIENT_SECRET=''
GITHUB_CLIENT_ID=''
GITHUB_CLIENT_SECRET=''
EMAIL_USER=''
EMAIL_PASSWORD=''
```
```commandline
# core.congif.py

username = os.environ.get('username')
password = os.environ.get('password')
database = os.environ.get('database')
port = os.environ.get('port')
host = os.environ.get('host')

SECRET_KEY = os.environ.get('SECRET_KEY')

GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

TWITTER_CLIENT_ID = os.environ.get('TWITTER_CLIENT_ID')
TWITTER_CLIENT_SECRET = os.environ.get('TWITTER_CLIENT_SECRET')

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
```

### Migrating Databases
```console
flask db upgrade
```

## Running the example

### Start redis backend
```commandline
$ redis-cli
redis 127.0.0.1:6379> ping
PONG
```

### Start a celery worker
You'll need a worker to get things done, run the following command in a separate terminal tab

```bash
celery worker -A celery_worker.celery --loglevel=info
```

### Start the app.

Open a new terminal tab and start the app

```bash
python run.py
```
or in linux
```commandline
export FLASK_APP=run.py
flask run
```
for windows and mac
```commandline
set FLASK_APP=run.py
flask run
```

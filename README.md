# Innodogs
Flask web application, intended to handle information about stray dogs.

This is a course project for Data Modeling and Databases course, so ORM using now is prohibited.

## How to launch:
Create database with the name `innodogs`
Create local config file `local.cfg` with the following (change only the first line accordingly):
```
SQLALCHEMY_DATABASE_URI='postgresql://username:password@localhost:5432/innodogs'
SECRET_KEY='secret'
GOOGLE_LOGIN_CLIENT_ID='822633610472-ke3kgvsi46g5q61tk92sdrk3ojutn5lq.apps.googleusercontent.com'
GOOGLE_LOGIN_CLIENT_SECRET='2gIql-eLNmhPtEcIXigUCo0x'
GOOGLE_LOGIN_REDIRECT_URI='http://localhost:5000/'
GOOGLE_LOGIN_REDIRECT_SCHEME='http'
UPLOAD_FOLDER='dogs'
```

Clone project, checkout `master2` branch and put `local.cfg` into `./app/` folder and run in terminal:
```sh
$ export LOCAL_CONFIG=local.cfg
$ pip3 install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ python3 run.py
...
^C
$ deactivate
```

#!/bin/bash

rm db.sqlite3
rm -rf ./diningapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations diningapi
python3 manage.py migrate diningapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens


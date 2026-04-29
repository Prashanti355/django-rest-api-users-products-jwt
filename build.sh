#!/usr/bin/env bash
set -o errexit

pip install -r requirements/production.txt

python app/manage.py collectstatic --no-input
python app/manage.py migrate
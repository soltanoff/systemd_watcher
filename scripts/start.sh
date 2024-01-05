#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python manage.py migrate
python manage.py collectstatic --no-input --clear
gunicorn --bind 0.0.0.0:8000 --workers 4 wsgi:application --timeout 600
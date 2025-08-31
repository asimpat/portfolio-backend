#!/usr/bin/env bash
# exit on error
set -o errexit  


pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

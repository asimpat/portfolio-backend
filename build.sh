#!/usr/bin/env bash
# exit on error
set -o errexit  


pip install -r requirements.txt

# Collect static files
python portfolio_project/manage.py collectstatic --noinput

# Run migrations
python portfolio_project/manage.py migrate


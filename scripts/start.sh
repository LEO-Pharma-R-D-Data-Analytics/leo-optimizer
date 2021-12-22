#!/usr/bin/env bash

# Setu up IP GATEWAY for django debug toolbar
export GATEWAY_IP=$(hostname -i | sed 's/.$/1/')

# Install dependencies
pip install --upgrade pip poetry
poetry update -vvv
poetry install

# Migrate and seed database
rm /src/app/db.sqlite3
poetry run python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | poetry run python manage.py shell

# Seed database
poetry run python manage.py seed

# Run server in foregroud
poetry run python manage.py runserver 0.0.0.0:8000

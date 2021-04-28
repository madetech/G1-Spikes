#!/usr/bin/env bash

# TODO maybe make separate scripts so we can choose to just install base wagtail, or the whole Shebang!


# Pull and Install Wagtail with Python Virtual Environment
./scripts/get_wagtail.sh

# Update default Wagtail Files to use Local DB - delete and replace existing values
./scripts/update_wagtail_db_envs.sh

# Expose the API


# Launch Docker-Compose
docker-compose up -d --build

# Create Admin User (uses .env.dev Superuser values)
echo "Creating default Super User"
docker-compose run --rm web python manage.py createsuperuser --noinput
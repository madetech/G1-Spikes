#!/usr/bin/env bash

# TODO maybe make separate scripts so we can choose to just install base wagtail, or the whole Shebang!


# Pull and Install Wagtail with Python Virtual Environment
# echo "Starting Virtual Environment..."
# python3 -m venv venv
# source venv/env/bin/activate
# echo "Installing Wagtail..."
# pip3 install --upgrade pip
# pip3 install wagtail
# wagtail start app TODO need to check doesn't already exist

# Update default Wagtail Files to use Local DB - delete and replace existing values
./scripts/update_wagtail_db_envs.sh

# Expose the API


# Launch Docker-Compose


# Create Admin User
# docker-compose run --rm web python manage.py createsuperuser
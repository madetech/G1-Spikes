#!/usr/bin/env bash

# Run this Script for the intial Setup, you can use docker-compose (or individual scripts) for subsequent usage

#  The scripts will:
# 1. Setup a Python virtual Environment
# 2. Install Wagtail to the Virtual Environment
# 3. Update the default files to use postgress DB instead of the default
# 4. Update the default files to Expose the API (see: https://docs.wagtail.io/en/stable/advanced_topics/api/v2/configuration.html)
# 5. Build a Wagtail docker Container
# 6. Run PostgreSQL Container and the Wagtail Container
# 7. Create a default Super User (see .env.dev for these values)


# Pull and Install Wagtail with Python Virtual Environment
./scripts/get_wagtail.sh


# Expose the API and SetupDB Config
./scripts/expose_wagtail_api_and_setup_db.sh

# Launch Docker-Compose
docker-compose up -d --build

# Create Admin User (uses .env.dev Superuser values)
echo "Creating default Super User"
docker-compose run --rm web python manage.py createsuperuser --noinput
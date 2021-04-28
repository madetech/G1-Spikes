#!/usr/bin/env bash

WAGTAIL_APP_ROUTE="app/app/"
WAGTAIL_API_FILE="api.py"
WAGTAIL_URL_FILE="urls.py"
WAGTAIL_BASE_FILE="base.py"
WAGTAIL_DEV_FILE="dev.py" # location of DB Config

# Coppy supporting files to correct directory 
cp ${PWD}/scripts/supportingPythonFiles/$WAGTAIL_API_FILE ${PWD}/$WAGTAIL_APP_ROUTE
cp ${PWD}/scripts/supportingPythonFiles/$WAGTAIL_URL_FILE ${PWD}/$WAGTAIL_APP_ROUTE
cp ${PWD}/scripts/supportingPythonFiles/$WAGTAIL_BASE_FILE ${PWD}/$WAGTAIL_APP_ROUTE/settings
cp ${PWD}/scripts/supportingPythonFiles/$WAGTAIL_DEV_FILE ${PWD}/$WAGTAIL_APP_ROUTE/settings

# Postgres Driver
echo "psycopg2-binary==2.8.6" >> ${PWD}/app/requirements.txt

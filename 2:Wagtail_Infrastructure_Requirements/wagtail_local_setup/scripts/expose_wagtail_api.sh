#!/usr/bin/env bash
set -x

WAGTAIL_APP_ROUTE="../app/app/"
WAGTAIL_API_FILE="api.py"
WAGTAIL_URL_FILE="urls.py"
WAGTAIL_SETTINGS_FILE="settings/base.py"

sed -i -E "/^INSTALLED_APPS =/a'wagtail.api.v2','rest_framework'," $WAGTAIL_APP_ROUTE$WAGTAIL_SETTINGS_FILE


# Update base.py


# Update urls.py


# Create api.py
cp ${PWD}/scripts/api.py ${PWD}/app/app/settings

cp ${PWD}/supportingPythonFiles/$WAGTAIL_API_FILE ${PWD}/app
cp ${PWD}/supportingPythonFiles/$WAGTAIL_URL_FILE ${PWD}/app

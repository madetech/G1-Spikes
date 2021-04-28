#!/usr/bin/env bash

WAGTAIL_APP_ROUTE="app/app/"
WAGTAIL_API_FILE="api.py"
WAGTAIL_URL_FILE="urls.py"
WAGTAIL_SETTINGS_FILE="settings/base.py"

sed -i -E "/^INSTALLED_APPS =/a'wagtail.api.v2','rest_framework'," $WAGTAIL_APP_ROUTE$WAGTAIL_SETTINGS_FILE

cp ./scripts/supportingPythonFiles/$WAGTAIL_API_FILE $WAGTAIL_APP_ROUTE$WAGTAIL_API_FILE
cp ./scripts/supportingPythonFiles/$WAGTAIL_URL_FILE $WAGTAIL_APP_ROUTE$WAGTAIL_URL_FILE
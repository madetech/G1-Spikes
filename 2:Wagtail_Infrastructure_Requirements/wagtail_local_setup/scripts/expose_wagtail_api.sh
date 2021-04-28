#!/usr/bin/env bash
set -x

# 'wagtail.api.v2',
# 'rest_framework',

# sed -i "/^INSTALLED_APPS = \[/a 'wagtail.api.v2'" app/app/settings/base.py

# sed -i -E '/^INSTALLED_APPS = \[/a\
# \'wagtail.api.v2\',' app/app/settings/base.py


# Update base.py


# Update urls.py


# Create api.py
cp ${PWD}/scripts/api.py ${PWD}/app/app/settings
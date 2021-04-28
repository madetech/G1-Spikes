#!/usr/bin/env bash

echo "Starting Virtual Environment..."
python3 -m venv venv
source venv/bin/activate
echo "Installing Wagtail..."
pip3 install --upgrade pip
pip3 install wagtail
wagtail start app
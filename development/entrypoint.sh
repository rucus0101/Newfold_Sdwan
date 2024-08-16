#!/bin/sh

# Installing git
echo "Installing dependencies"
apk add --no-cache git git-fast-import

# Making /data and /site safe for git
git config --global --add safe.directory /data
git config --global --add safe.directory /site

# install pip requirements
echo "Installing Python requirements"
pip install -r ansible_collections/arista/avd/docs/requirements.txt --upgrade

# Start mkdocs
echo "Starting mkdocs"
mkdocs serve --no-livereload --dev-addr=0.0.0.0:8000 -f mkdocs.yml

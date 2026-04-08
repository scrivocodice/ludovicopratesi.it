#!/bin/sh

set -eu

APP_DIR="/srv/apps/ludovicopratesi"
VENV_DIR="/srv/venvs/ludovicopratesi"
ENV_FILE="${APP_DIR}/.env.production"

cd "${APP_DIR}"

set -a
. "${ENV_FILE}"
set +a

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-www.settings.prod}"

exec "${VENV_DIR}/bin/gunicorn" \
    www.wsgi:application \
    --bind 127.0.0.1:8002 \
    --workers 3 \
    --timeout 60

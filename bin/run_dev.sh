#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)
VENV_DIR=${VENV_DIR:-"${PROJECT_ROOT}/.venv"}
PYTHON_BIN=${PYTHON_BIN:-"${VENV_DIR}/bin/python"}
REQUIREMENTS_FILE="${PROJECT_ROOT}/etc/requirements/dev.txt"
HOST=${HOST:-127.0.0.1}
PORT=${PORT:-8000}

if [ ! -x "${PYTHON_BIN}" ]; then
  python3 -m venv "${VENV_DIR}"
fi

if ! "${PYTHON_BIN}" -c "import django" >/dev/null 2>&1; then
  "${PYTHON_BIN}" -m pip install -r "${REQUIREMENTS_FILE}"
fi

# A dev launcher should not inherit a stale settings module from the shell.
export DJANGO_SETTINGS_MODULE=www.settings.loc
export PYTHONUNBUFFERED=1

cd "${PROJECT_ROOT}"

if [ "$#" -eq 0 ]; then
  set -- "${HOST}:${PORT}"
fi

exec "${PYTHON_BIN}" manage.py runserver "$@"

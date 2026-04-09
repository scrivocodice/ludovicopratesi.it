#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "${SCRIPT_DIR}/.." && pwd)

APP_DIR=${APP_DIR:-"${PROJECT_ROOT}"}
VENV_DIR=${VENV_DIR:-"/srv/venvs/ludovicopratesi"}
PYTHON_BIN=${PYTHON_BIN:-"${VENV_DIR}/bin/python"}
ENV_FILE=${ENV_FILE:-"${APP_DIR}/.env.production"}
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-"www.settings.prod"}
SUPERVISOR_ACTION=${SUPERVISOR_ACTION:-"reload"}
SUPERVISOR_PROGRAM=${SUPERVISOR_PROGRAM:-"ludovicopratesi"}

log() {
  printf '[deploy] %s\n' "$1"
}

run_supervisorctl() {
  if supervisorctl "$@"; then
    return 0
  fi

  if command -v sudo >/dev/null 2>&1; then
    log "supervisorctl failed without sudo, retrying with sudo"
    sudo supervisorctl "$@"
    return 0
  fi

  return 1
}

if [ ! -f "${ENV_FILE}" ]; then
  printf 'Missing environment file: %s\n' "${ENV_FILE}" >&2
  exit 1
fi

if [ ! -x "${PYTHON_BIN}" ]; then
  printf 'Missing Python executable: %s\n' "${PYTHON_BIN}" >&2
  exit 1
fi

cd "${APP_DIR}"

log "Pulling latest code"
git pull --ff-only

log "Loading production environment"
set -a
. "${ENV_FILE}"
set +a

export DJANGO_SETTINGS_MODULE

log "Collecting static files"
"${PYTHON_BIN}" manage.py collectstatic --settings="${DJANGO_SETTINGS_MODULE}" --noinput

case "${SUPERVISOR_ACTION}" in
  reload)
    log "Reloading supervisord"
    run_supervisorctl reload
    ;;
  restart)
    log "Restarting supervisor program ${SUPERVISOR_PROGRAM}"
    run_supervisorctl restart "${SUPERVISOR_PROGRAM}"
    ;;
  *)
    printf 'Unsupported SUPERVISOR_ACTION: %s\n' "${SUPERVISOR_ACTION}" >&2
    exit 1
    ;;
esac

log "Deploy completed"

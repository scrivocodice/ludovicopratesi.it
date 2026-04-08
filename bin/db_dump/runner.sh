#!/bin/sh

set -eu

#
# This script dumps your database in a folder on your server.
#
# Set your cron to schedule dump periodically
#

# ==========
# Variables
# ==========

# Set your database name
DB_NAME="${DB_NAME:-ludovicopratesi_db}"

# Set your system's path where store dumps (add final /)
DB_DUMPS_DIR="${DB_DUMPS_DIR:-/srv/backups/}"

# Set your dump command
DB_DUMP_COMMAND="${DB_DUMP_COMMAND:-/usr/bin/pg_dump}"

# Set the system user that can access PostgreSQL locally.
# Leave empty to use application credentials instead.
DB_SYSTEM_USER="${DB_SYSTEM_USER:-postgres}"

# Application database connection settings used when DB_SYSTEM_USER is empty.
DB_HOST="${DB_HOST:-127.0.0.1}"
DB_PORT="${DB_PORT:-5432}"
DB_USER="${DB_USER:-ludovicopratesi_usr}"
DB_PASSWORD="${DB_PASSWORD:-}"
DB_PASSFILE="${DB_PASSFILE:-}"

# Set your compression command
ZIP_COMMAND="${ZIP_COMMAND:-/bin/gzip}"

# Get the current datatime
CURRENT_DATETIME="$(date +%Y%m%d%H%M%S)"

# ==========
# Execution
# ==========

echo "$(date +%Y%m%d%H%M%S) - BEGIN execution."

dump_name="${CURRENT_DATETIME}.${DB_NAME}.dump.sql";
dump_path="${DB_DUMPS_DIR}${dump_name}";

mkdir -p "${DB_DUMPS_DIR}";

# Database's dump
if [ -n "${DB_SYSTEM_USER}" ]; then
    /usr/bin/sudo -u "${DB_SYSTEM_USER}" "${DB_DUMP_COMMAND}" "${DB_NAME}" > "${dump_path}";
    echo "$(date +%Y%m%d%H%M%S) - Dumped db with command: /usr/bin/sudo -u ${DB_SYSTEM_USER} ${DB_DUMP_COMMAND} ${DB_NAME} > ${dump_path}"
else
    if [ -n "${DB_PASSWORD}" ]; then
        PGPASSWORD="${DB_PASSWORD}" "${DB_DUMP_COMMAND}" -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" "${DB_NAME}" > "${dump_path}";
    elif [ -n "${DB_PASSFILE}" ]; then
        PGPASSFILE="${DB_PASSFILE}" "${DB_DUMP_COMMAND}" -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" "${DB_NAME}" > "${dump_path}";
    else
        "${DB_DUMP_COMMAND}" -h "${DB_HOST}" -p "${DB_PORT}" -U "${DB_USER}" "${DB_NAME}" > "${dump_path}";
    fi
    echo "$(date +%Y%m%d%H%M%S) - Dumped db with command: ${DB_DUMP_COMMAND} -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} ${DB_NAME} > ${dump_path}"
fi

# Dump compression using gzip
${ZIP_COMMAND} "${dump_path}";
echo "$(date +%Y%m%d%H%M%S) - Compressing dump with command: ${ZIP_COMMAND} ${dump_path}"

echo "$(date +%Y%m%d%H%M%S) - END execution."
echo ""

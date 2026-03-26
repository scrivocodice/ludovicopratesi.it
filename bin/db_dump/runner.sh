#!/bin/bash

#
# This script dumps your database in a folder on your server.
#
# Set your cron to schedule dump periodically
#

# ==========
# Variables
# ==========

# Set your database name
DB_NAME='ludovicopratesi_db';

# Set your system's path where store dumps (add final /)
DB_DUMPS_DIR="/home/ludovicopratesi/var/db_dumps/";

# Set your dump command
DB_DUMP_COMMAND='/usr/bin/pg_dump';

# Set your compression command
ZIP_COMMAND='/bin/gzip';

# Get the current datatime
CURRENT_DATETIME=`date +%Y%m%d%H%M%S`;

# ==========
# Execution
# ==========

echo "`date +%Y%m%d%H%M%S` - BEGIN execution.";

dump_name="${CURRENT_DATETIME}.${DB_NAME}.dump.sql";
dump_path="${DB_DUMPS_DIR}${dump_name}";

# Database's dump
"${DB_DUMP_COMMAND}" "${DB_NAME}" > "${dump_path}";
echo "`date +%Y%m%d%H%M%S` - Dumped db with command: ${DB_DUMP_COMMAND} ${DB_NAME} > ${dump_path}";

# Dump compression using gzip
${ZIP_COMMAND} "${dump_path}";
echo "`date +%Y%m%d%H%M%S` - Compressing dump with command: ${ZIP_COMMAND} ${dump_path}";

echo "`date +%Y%m%d%H%M%S` - END execution.";
echo ""

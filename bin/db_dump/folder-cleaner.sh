#!/bin/bash

#
# Rotate dump in a folder keeping the number you want to have stored.
#
# author: Piergiorgio Faraglia (http://piergiorgiofaraglia.it)
#

# ==========
# Variables
# ==========

# Set your db dump folder
BASEDIR="/home/ludovicopratesi";

# Set maximum number of dump you want stored in folder
KEEP_ALIVE_DUMPS=10;

# Set your system's path where store dumps (add final /)
DB_DUMPS_DIR="${BASEDIR}/var/db_dumps/";

# Get the current datatime
CURRENT_DATETIME=`date +%Y%m%d%H%M%S`;

# ==========
# Execution
# ==========

echo "`date +%Y%m%d%H%M%S` - BEGIN execution.";

NUM_DUMPS=`ls -1 "${DB_DUMPS_DIR}" | wc -l`
DUMP_TO_DELETE=$(echo "${NUM_DUMPS}-${KEEP_ALIVE_DUMPS}"|bc)

if [ ${DUMP_TO_DELETE} -le 0 ]; then
    echo "`date +%Y%m%d%H%M%S` - No exceeded dump found. Nothing to delete."
else
    for i in `ls -1 ${DB_DUMPS_DIR} | head -${DUMP_TO_DELETE}`; do
        echo "`date +%Y%m%d%H%M%S` - removing item: ${BASEDIR}$i."
        rm -v "${DB_DUMPS_DIR}$i"
    done
fi

echo "`date +%Y%m%d%H%M%S` - END execution.";
echo ""

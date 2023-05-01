#!/bin/sh
SCRIPT_DIR=$(busybox dirname "$0")
PYTHONPATH=${SCRIPT_DIR}/Python
HOME=${SCRIPT_DIR}/sample
PROG_PATH=${HOME}/sample_app.py
export LD_LIBRARY_PATH="${PYTHONPATH}/lib"
cd ${PYTHONPATH}
./python3.10 ${PROG_PATH}
sync

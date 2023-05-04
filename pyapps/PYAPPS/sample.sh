#!/bin/sh
SCRIPT_DIR=$(busybox dirname "$0")
PYTHONPATH=${SCRIPT_DIR}/Python
HOME=${SCRIPT_DIR}/sample
PROG_PATH=${HOME}/sample_app.py
cd ${PYTHONPATH}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(busybox pwd)/lib
./python3.10 ${PROG_PATH}
sync

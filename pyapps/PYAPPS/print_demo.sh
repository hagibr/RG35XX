#!/bin/sh
SCRIPT_DIR=$(busybox dirname "$0")
PYTHONPATH=${SCRIPT_DIR}/Python
HOME=${SCRIPT_DIR}/framebuffer
PROG_PATH=${HOME}/logging.py
export LD_LIBRARY_PATH="${PYTHONPATH}/lib"
cd ${PYTHONPATH}
busybox fbset -depth 16
./python3.10 ${PROG_PATH}
sync

#!/bin/sh
SCRIPT_DIR=$(busybox dirname "$0")
PYTHONPATH=${SCRIPT_DIR}/Python
HOME=${SCRIPT_DIR}/fbtft_test
PROG_PATH=${HOME}/test_fb.py
export LD_LIBRARY_PATH="${PYTHONPATH}/lib"
cd ${PYTHONPATH}
busybox fbset -depth 16
./python3.10 ${PROG_PATH}
sync


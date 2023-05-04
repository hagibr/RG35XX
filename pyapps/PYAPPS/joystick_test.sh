#!/bin/sh
SCRIPT_DIR=$(busybox dirname "$0")
PYTHONPATH=${SCRIPT_DIR}/Python
HOME=${SCRIPT_DIR}/joystick
PROG_PATH=${HOME}/joystick_test.py
cd ${PYTHONPATH}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(busybox pwd)/lib
./python3.10 ${PROG_PATH}
sync


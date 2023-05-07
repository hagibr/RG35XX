#!/system/bin/sh

# Simple script to help running Python REPL when using ADB Shell
# It can also run a python script if you give a file as argument
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(busybox pwd)/lib
./python3.10 $1

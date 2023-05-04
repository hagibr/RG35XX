#!/system/bin/sh

# Usage: ./.exec_script_in_adb.sh appscript.sh
# Example: ./.exec_script_in_adb.sh fbtft_test.sh

# Saving current directory
CUR_HOME=$(pwd)
# Setting environment the same way it's done in MISC/dmenu.bin
CFWROOT=/mnt/mmc/CFW
ROOTFS_MOUNTPOINT=/cfw
export PATH=/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH
export HOME=$CFWROOT
export SHELL=/bin/sh
export SDL_NOMOUSE=1

# Starting the application  
cd $HOME
busybox chroot $ROOTFS_MOUNTPOINT $CUR_HOME/$1


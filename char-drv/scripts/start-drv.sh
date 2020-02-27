#!/bin/bash

error_and_exit() {
	echo -ne "(!) $1\n"
	exit $2
}

if [ $(id -u) -ne 0 ]
then
	error_and_exit "Please run script as root." 1
fi

if [ -z "$1" ]
then
	error_and_exit "Please specify number of devices." 2
fi

NUM_REGEX='^[0-9]+$'
if ! [[ "$1" =~ $NUM_REGEX ]]
then
	error_and_exit "Please use a numeric value." 3
fi

if [ $1 -le 0 ]
then
	error_and_exit "Number of devices has to be at least one." 4
fi

if [ -z "$2" ]
then
	error_and_exit "Please pass user:group as second argument." 5
fi

USRGRP_REGEX='^\w+:\w+$'
if ! [[ "$2" =~ $USRGRP_REGEX ]]
then
	error_and_exit "Invalid argument: $2. Please use user:group format." 6
fi

insmod char-drv.ko device_num=$1

if [ $? -ne 0 ]
then
	error_and_exit "Could not start char-drv." 7
fi

MAJOR=`cat /proc/devices | awk '{ if($2=="char-drv") { print $1; exit 0 }; }'`

if [ -z "$MAJOR" ]
then
	rmmod char-drv.ko
	error_and_exit "Could not extract major number from /proc/devices." 8
fi

seq 1 1 $1 | awk \
	-v major=$MAJOR \
	-v usrgrp=$2 \
'{
	minor=$1 - 1
	dev_name="/dev/char-drv-" minor
	system("rm -rf" OFS dev_name)
	system("mknod" OFS dev_name OFS "c" OFS major OFS minor)
	system("chown" OFS usrgrp OFS dev_name)
}'

echo -ne "(i) Created devices:\n"

ls /dev | grep "char-drv" | awk '{
	file="\t/dev/" $1
	system("stat -c \"%A %U:%G %n\"" OFS file)
}'

exit 0

#!/bin/bash

error_and_exit() {
	echo -ne "(!) $1\n"
	exit $2
}

if [ -z "$COMM" ]
then
	COMM=insmod
fi

if [ $(id -u) -ne 0 ]
then
	error_and_exit "Please run script as root." 1
fi

if [ -z $1 ]
then
	error_and_exit "Please specify number of devices." 2
fi

echo $1 | grep '^[0-9]\+$' > /dev/null
if [ $? -ne 0 ]
then
	error_and_exit "Please use a numeric value." 3
fi

if [ $1 -le 0 ]
then
	error_and_exit "Number of devices has to be at least one." 4
fi

if [ -z $2 ]
then
	error_and_exit "Please pass user:group as second argument." 5
fi

echo $2 | grep '^\w\+:\w\+$' > /dev/null
if [ $? -ne 0 ]
then
	error_and_exit "Invalid argument: $2. Please use user:group format." 6
fi

if [ -z $3 ]
then
	error_and_exit "Please pass module name as third argument." 7
fi

echo $3

echo $3 | grep '^.*\.ko$' > /dev/null
if [ $? -ne 0 ]
then
	error_and_exit "The module name should end with .ko extension." 8
fi

$COMM $3 device_num=$1

if [ $? -ne 0 ]
then
	error_and_exit "Could not start $3 module." 9
fi

MAJOR=`awk -v dev_pref=${3%*.ko} '{
	if($2==dev_pref) {
		print $1
		exit 0
	}
}' /proc/devices`

if [ -z "$MAJOR" ]
then
	rmmod $3
	error_and_exit "Could not extract major number from /proc/devices." 10
fi

seq 1 1 $1 | awk \
	-v major=$MAJOR \
	-v usrgrp=$2 \
	-v dev_pref=${3%*.ko} \
'{
	minor=$1 - 1
	dev_name="/dev/" dev_pref "-" minor
	system("rm -rf" OFS dev_name)
	system("mknod" OFS dev_name OFS "c" OFS major OFS minor)
	system("chown" OFS usrgrp OFS dev_name)
}'

echo -ne "(i) Created devices:\n"

ls /dev | grep "${3%*.ko}" | awk '{
	file="\t/dev/" $1
	system("stat -c \"%A %U:%G %n\"" OFS file)
}'

exit 0

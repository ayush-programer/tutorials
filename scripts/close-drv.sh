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
	error_and_exit "Please pass module name as an argument." 2
fi

MODULE_REGEX='\w\.ko$'
if ! [[ "$1" =~ $MODULE_REGEX ]]
then
	error_and_exit "The module name should end with .ko extension." 3
fi

rmmod $1

ls /dev | grep "${1%*.ko}" | awk '{
	print "(i) Removing /dev/" $1
	system("rm -rf /dev/" $1)
}'

exit 0

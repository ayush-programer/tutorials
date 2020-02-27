#!/bin/bash

if [ $(id -u) -ne 0 ]
then
	echo -ne "(!) Please run script as root.\n"
	exit 1
fi

rmmod char-drv.ko

ls /dev | grep "char-drv" | awk '{
	print "(i) Removing /dev/" $1
	system("rm -rf /dev/" $1)
}'

exit 0

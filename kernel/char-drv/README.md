# Simple character device driver example

This simple example of a character device driver will print out to `dmesg` everything written to one of its device files `/dev/char-drv-<num>`. If these files are read (with `cat`, for example), you should get a literal output of `nothing`.

You can control the number of devices created by using:

`make start DEVICE_NUM=<num>`

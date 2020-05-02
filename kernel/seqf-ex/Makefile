obj-m = seqf-ex.o

KERNEL_SRC ?= /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd)

modules_install:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd) modules_install

clean:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd) clean

start: all
	sudo insmod $(basename $(obj-m)).ko

stop:
	sudo rmmod $(basename $(obj-m)).ko

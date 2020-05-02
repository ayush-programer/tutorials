obj-m = char-drv-ll.o
header-y = test.h
DEVICE_NUM ?= 4

KERNEL_SRC ?= /lib/modules/$(shell uname -r)/build

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd)

modules_install:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd) modules_install

clean:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd) clean

start: all
	sudo ../scripts/start-drv.sh $(DEVICE_NUM) $(shell id -un):$(shell id -gn) $(basename $(obj-m)).ko

stop:
	sudo ../scripts/close-drv.sh $(basename $(obj-m)).ko

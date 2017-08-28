KVER := $(shell uname -r)
KDIR := /usr/src/linux-headers-$(KVER)
PWD  := $(shell pwd)

obj-m += vtkbd.o

default:
	$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules

clean:
	@rm -Rf *.o *.ko *.mod.c modules.order Module.symvers Module.markers

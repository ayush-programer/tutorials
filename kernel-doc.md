# Linux Kernel Hacking

## printk

To print a message to DMESG, use:

```c
printk(KERN_INFO "<message>", ...);
```

Note: There is no comma after `KERN_INFO`. This is the intended way this macro was defined.

There are various log levels (if not specified, `DEFAULT_MESSAGE_LOGLEVEL` will be used; check `linux/kernel.h`), but to make sure that the message reaches `DMESG`, use:

```c
pr_err("<message>");
```

### log level

| lvl |     string     |                     meaning                     |
|-----|----------------|-------------------------------------------------|
|  0  | `KERN_EMERG`   | emergency messages (pre-crash)                  |
|  1  | `KERN_ALERT`   | situation requiring immediate action            |
|  2  | `KERN_CRIT`    | serious hardware or software failures           |
|  3  | `KERN_ERR`     | usually hardware issues by drivers              |
|  4  | `KERN_WARNING` | problematic situation                           |
|  5  | `KERN_NOTICE`  | normal situation or security related            |
|  6  | `KERN_INFO`    | informational messages (driver info on startup) |
|  7  | `KERN_DEBUG`   | debugging messages                              |

Note: You can check the log level by typing:

```shell
cat /proc/sys/kernel/printk
```

To get full meaning of the four numbers, use:

```shell
cat /proc/sys/kernel/printk | awk '{ OFS="|"; print "current loglevel:" OFS $1; print "default loglevel:" OFS $2; print "minimum loglevel:" OFS $3; print "boot-time default loglevel:" OFS $4;  }' | column -t -s'|'
```

### printk rate limit

Note: You can also limit the number of `printk` messages:

```c
if (printk_ratelimit())
	printk(...);
```

The function is defined as:

```c
int printk_ratelimit(void);
```

The rate limit can be customized via the two files in `/proc/sys/kernel`:

|           file           |                        meaning                        |
|--------------------------|-------------------------------------------------------|
| `printk_ratelimit`       | number of seconds to wait before re-enabling messages |
| `printk_ratelimit_burst` | number of messages received before rate-limiting      |

## current process

Pointer to the `task struct` of the current process is `current`; so mostly anywhere in the kernel code, you can write things such as:

```c
printk(KERN_INFO "%s, %d", current->comm, current->pid);
```

Note: This is imported from `linux/sched.h`.

## container of

Assume you have a structure like this:

```c
struct test_struct {
	type_1 var_1;
	type_2 var_2;
	...
	type_n var_n;
};

struct test_struct test;
```

You can get the pointer to `test` from any `var_k` (assume we have `var_k_ptr` that points to it) by using:

```c
struct test_struct *test_ptr;

test_ptr = container_of(var_k_ptr, struct test_struct, var_k);
```

## exporting symbols

If you want the symbols, i.e. functions, variables, etc. to be available to other parts of kernel or modules, you can use:

```c
EXPORT_SYMBOL(name);
```

There is a variant:

```
EXPORT_SYMBOL_GPL(name);
```

This one will make the symbol available to GPL-licensed modules only.

## kmalloc

The general syntax is:

```c
kmalloc(size_t size, gfp_t flags);
```

Import the header `linux/slab.h`.

## user-space and kernel-space

### compiler information

In `C`, you can easily distinguish whether your code is run in kernel-space or user-space context with `__KERNEL__` macro:

```c
#ifdef __KERNEL__
	/* code for kernel-space */
#else
	/* code for user-space */
```

### data exchange

Import `linux/uaccess.h`.

To copy from user-space to kernel-space:

```c
unsigned long copy_from_user (void* to, const void __user* from, unsigned long n);
```

Note: The `__user` macro is only there to tell that we are dealing with untrusted pointer (from user-space). It only makes sense from the context of kernel development tools like `sparse`.

To copy from kernel-space to user-space:

```c
unsigned long copy_to_user (void __user* to, const void* from, unsigned long n);
```

## linked lists

### definition

This is a definition of `list_head` from `include/linux/types.h`:

```c
struct list_head {
	struct list_head *next, *prev;
};
```

Each node can be part of multiple linked lists:

```c
struct node_el {
	int data;
	list_head list1;
	list_head list2;
	list_head list3;
};
```

This is why definition of linked list is "upside down" in the kernel, i.e. why `list_head` is inside `struct node_el`, and not vice versa (this is really more of a graph than a linked list). The rest of linked list code can be found in `include/linux/list.h`.

### intialization

To declare and initialize the linked list:

```c
struct list_head my_list;
INIT_LIST_HEAD(&my_list);
```

Note: You can also use:

```c
LIST_HEAD(my_list);
```

This will initialize the list at compile time.

### add an element

To add an element to a linked list, first define a pointer to `struct node_el`:

```c
struct node_el *new_el;
```

After filling out the data (except for `list_head` variables), do:

```c
list_add(&new_el->list1, &my_list);
```

This is great for implementing stacks. For queues, try:

```c
list_add_tail(&new_el->list1, &my_list);
```

### iterate over list

```c
struct list_head *ptr;
struct node_el *entry;

list_for_each(ptr, &my_list) {
	entry = list_entry(ptr, struct node_el, list1);
}
```

### deinitialize

To delete an element from the list:

```c
list_del(entry);
```

To delete the whole list, just iterate over the list deleting nodes.

## kernel modules

### hello world module

Create a project folder with following files:

```
hello.c
Makefile
```

In `hello.c` type the following:

```c
#include <linux/module.h>

char name = "world";

static int __init hello_start(void)
{
	pr_err("Hello, %s!\n", name);
	// code to run on insmod
	return 0;
}

static void __exit hello_end(void)
{
	pr_err("Goodbye, %s!\n", name);
	// code to run on rmmod
}

module_param(name, charp, S_IRUGO);
module_init(hello_start);
module_exit(hello_end);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("My first module");
MODULE_VERSION("0.1");
```

For `Makefile` you can use:

```make
obj-m = hello.o

KERNEL_SRC ?= /lib/modules/$(shell uname-r)/build

all:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd)

modules_install:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd) modules_install

clean:
	$(MAKE) -C $(KERNEL_SRC) M=$(shell pwd) clean
```

Then, in your project folder just type `make`. To enable this kernel module, just type:

```shell
sudo insmod hello.ko
```

Now check out the `dmesg`!

Note: This `Makefile` example will also work automatically for Yocto build.

To remove the kernel module, do:

```shell
sudo rmmod hello.ko
```

You should notice the `module_param` that exposes `char name` variable as a module parameter. You can try running `insmod` with your name as a parameter:

```shell
sudo insmod hello.ko name="Stjepan"
```

You should see your "Hello, Stjepan!" in `dmesg` now. Also, to see a list of available parameters for your module, try:

```shell
ls /sys/module/<module_name>/parameters
```

In this example, to read it (this is what `S_IRUGO` flag allows), just do:

```shell
$ cat /sys/module/hello/parameters/name
Stjepan
```

If instead of `S_IRUGO` there was `0`, this file would not be exposed, i.e. user would not be able to read this parameter at runtime. Also note that, as a second argument, `module_param` also accepts these values:

|             |             |             |
|-------------|-------------|-------------|
| `bool`      | `short`     | `int`       |
| `invbool`   | `uint`      | `long`      |
| `charp`     | `ulong`     | `ushort`    |
| `int`       | `long`      | `intarray`  |

### simple hrtimer example

We will simply expand on the previous example.

```c
#include <linux/module.h>
#include <linux/hrtimer.h>
#include <linux/ktime.h>

static struct hrtimer my_hrtimer;
ktime_t my_ktime;
char* name = "world";

// timer callback function
enum hrtimer_restart timer_callback(struct hrtimer *timer)
{
	pr_err("Hello, %s!\n", name);

	// code to run on timer expire

	// forward the timer expiry
	hrtimer_forward_now(timer, my_ktime);

	return HRTIMER_RESTART;
}

static int __init hrt_start(void)
{
	// ktime_set(sec, nsec); here it is 2.5 seconds
	my_ktime = ktime_set(2, 5000000);

	hrtimer_init(&my_hrtimer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
	my_hrtimer.function = &timer_callback;
	hrtimer_start(&my_hrtimer, my_ktime, HRTIMER_MODE_REL);

	return 0;
}

static void __exit hrt_end(void)
{
	pr_err("Goodbye, %s!\n", name);
	hrtimer_cancel(&my_hrtimer);
}

module_param(name, charp, S_IRUGO|S_IWUSR);
module_init(hrt_start);
module_exit(hrt_end);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("hrtimer example");
MODULE_VERSION("0.1");
```

This code will run `timer_callback` every `2.5` seconds. Try:

```shell
dmesg -w
```

And in other terminal window, do:

```shell
sudo insmod hello.ko name="Stjepan"
```

You should see the message repeated every `2.5` seconds.

You will also notice that here we typed `S_IRUGO|S_IWUSR` as third argument of the `module_param`. The `S_IWUSR` allows superuser to change the parameter at runtime! Try:

```shell
sudo bash -c 'echo -n "Stjepan" >> /sys/module/hello/parameters/name'
```

Note: This may cause concurrency issues, so avoid using it altogether (but it's fun to play with).

Check for more useful `hrtimer` functions in `include/linux/hrtimer.h`.

### char driver

#### major and minor numbers

You can see the list of character devices on your system along with their major and minor device numbers:

```shell
ls -l /dev | grep -E '^c' | gawk '{ for(i=1; i<=10; i++) { if (i==5) { printf "\033[1m\033[34m"; } else if (i==7) { printf "\033[m"; }; if (i < 10) { printf $i OFS; } else { print $i; } } }' | column -t
```

The major number identifies the driver associated with the device (for example, major `4` is for terminal devices). The minor number is for specific device (no rules about this one).

In the kernel module, you can obtain the device number (minor) with one of the following functions (from `linux/kdev_t.h`):

```c
int print_dev_t(char* buffer, dev_t dev);
char* format_dev_t(char* buffer, dev_t dev);
```

#### protocol

First step is to define the `file_operations` struct and corresponding functions. This is minimal recommended:

```c
static int char_drv_open(struct inode* inode, struct file* filp);
static int char_drv_release(struct inode* inode, struct file* filp);
static ssize_t char_drv_read(struct file* filp, char* buff, size_t size, loff_t* loff);
static ssize_t char_drv_write(struct file* filp, const char* buff, size_t size, loff_t* loff);

static struct file_operations char_fops = {
	.owner		= THIS_MODULE,
	.open		= char_drv_open,
	.release	= char_drv_release,
	.read		= char_drv_read,
	.write		= char_drv_write,
};
```

Note: You can find the full and latest list of `struct file_operations` function pointers [here](https://elixir.bootlin.com/linux/latest/source/include/linux/fs.h#L1821).

#### file

You can find the latest reference on `struct file` [here](https://elixir.bootlin.com/linux/latest/source/include/linux/fs.h#L935).

## syscalls

### add new syscall

First, create a folder `hello` in kernel repo root folder containing two files:

```
hello.c
Makefile
```

In `Makefile`, type:

```make
obj-y := hello.o
```

The `hello.c` file should look like this:

```c
#include <linux/kernel.h>

asmlinkage long sys_hello(void)
{
	// syscall code

	return 0;
}
```

Then, edit the `core-y` line in the `Makefile` in the kernel repo root folder to include `hello/`:

```make
core-y += kernel/ mm/ fs/ ipc/ security/ crypto/ block/ samples/ hello/
```

Finally, add the declaration of your system call in `include/linux/syscalls.h`:

```C
asmlinkage long sys_hello(void);
```

The rest is platform-specific.

#### arm

First, find any `CALL(sys_ni_syscall)` entry in `arch/arm/kernel/calls.S` and replace it with `CALL(sys_hello)`. You can see what system call number it will be based on commented out padding numbers. For example, our system call number for this example will be `313`:

```
/* 310 */	CALL(sys_request_key)
		CALL(sys_keyctl)
		CALL(ABI(sys_semtimedop, sys_oabi_semtimedop))
		CALL(sys_hello)
		CALL(sys_ioprio_set)
```

Second, in `arch/arm/include/uapi/asm/unistd.h`, add your system call to the bottom of the table:

```C
#define __NR_memfd_create		(__NR_SYSCALL_BASE+385)
#define __NR_bpf			(__NR_SYSCALL_BASE+386)
#define __NR_execveat			(__NR_SYSCALL_BASE+387)
#define __NR_hello			(__NR_SYSCALL_BASE+388)
```

In `/arch/arm64/include/asm/unistd32.h` (common for 32bit and 64bit), find your system call number (e.g. 313 for our needs), and rename it accordingly:

```C
#define __NR_semtimedop 312
__SYSCALL(__NR_semtimedop, compat_sys_semtimedop)
#define __NR_hello 313
__SYSCALL(__NR_hello, sys_hello)
#define __NR_ioprio_set 314
__SYSCALL(__NR_ioprio_set, sys_ioprio_set)
#define __NR_ioprio_get 315
```

Note that all of this might vary, but could give you a good insight in how to add a new system call.

#### x86

Just edit `arch/x86/syscalls/syscall_64.tbl` and arch/x86/syscalls/syscall_32.tbl`, and add your system call to the end of the list.

### syscall from shell

#### using Python

For example, on `x86` architecture, you can try:

```shell
$ python -c "import ctypes; ctypes.CDLL(None).syscall(1, 0, b'Hello world\x21\x0A', 13);"
Hello world!
```

Also, for something more simple (get pid of current process - in this case of `python`):

```shell
$ python -c "import ctypes; print ctypes.CDLL(None).syscall(39);"
28962
```

Note: This requires the `ctypes` library so it is not guaranteed to work.

#### using Perl

In lieu of the Python examples above, you can also try the following:

```shell
$ perl -e '$var="Hello world!\n"; syscall(1, 0, $var, 13);
Hello world!
```

Also, for `getpid`:

```shell
$ perl -e 'print syscall(39);'
13155
```

### syscall in C

This is an example of a system call in C:

```c
#include <unistd.h>
#include <sys/syscall.h>

int main(void) {

	syscall(SYS_write, 1, "Hello world!\n", 13);

	return 0;
}
```

# Kernel Debugging



## gdb

First, load vmlinux with debug symbols into gdb:

```shell
gdb <path_to_vmlinux>
```

Then, if, e.g. PC is at address `0xc081d0f8`, just type in:

```gdb
info line *0xc081d0f8
```

If the address is valid, you should be able to get the exact line of code where exception happened.

# Yocto

Before doing anything else, clone `poky`:

```shell
git clone git://git.yoctoproject.org/poky
```

You can choose the version that suits your needs on this [link](https://git.yoctoproject.org/cgit/cgit.cgi/poky/). Then, check it out. For example:

```shell
git checkout warrior
```

Before doing anything, be sure to position yourself in the `poky` folder and run:

```shell
source oe-init-build-dev
```

This will reposition you in the `poky/build` folder. The most important files here are `local.conf` and `bblayers.conf` in the `conf` subfolder.

## layers

All layers are stored in the `poky` folder and are named beginning withi the `meta-` keyword.

## list recipes

The following command will give you a list of recipes, along with their corresponding layer:

```shell
bitbake-layers show-recipes
```

## qemu

After you build the image, you can run it in `qemu` using:

```shell
runqemu <machine> [nographic]
```

The `<machine>` variable is the one you have set in `build/conf/local.conf` as the `MACHINE` variable. To be sure to be able to run `qemu`, you can use `qemuarm`, `qemuarm64` or `qemux86` for `MACHINE`, to name a few.

## add new recipe

To add a new recipe named "example" add the `example` subfolder in the layer of your choice and there add the file `example_01.bb`. There are multiple ways to write a recipe, so we will cover a few, depending on the build system used.

### common

An ordinary recipe should contain this as a header:

```shell
SUMMARY = "Short summary"
DESCRIPTION = "If description is empty, summary will be used."
AUTHOR = "Stjepan Poljak <stjepan.poljak@protonmail.com>"
HOMEPAGE = "https://github.com/StjepanPoljak"

SECTION = "examples"
DEPENDS = ""
PRIORITY = "optional"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"
```

You can check all these variables out on this [link](https://www.yoctoproject.org/docs/latest/ref-manual/ref-manual.html).

## add new layer

To add new layer, after running `source oe-init-build-end`, return to the poky folder and run:

```shell
bitbake-layers create-layer <layer_name>
``` 

It is customary to prefix the layer name with `meta-` keyword. This will create a simple folder structure for your layer. To add the new layer to the build, type in the `build` subfolder:

```shell
bitbake-layers add-layer <layer_name>
```

Or, even better, edit the `build/conf/bblayers.conf` to include your layer.

## add new image

Here is an example of an image recipe that inherits `core-image` and includes `core-image-minimal`:

```shell
SUMMARY = "Custom image"

LICENSE = "MIT"

inherit core-image
require recipes-core/images/core-image-minimal.bb

CORE_IMAGE_EXTRA_INSTALL = "example"
```

It is customary to put the `<image_name>.bb` file in the `<layer>/recipes-core/images/<image_name>` folder. The path in `require` line is necessary if you are including an image from another layer.

Add your recipes to the `CORE_IMAGE_EXTRA_INSTALL` variable (here we only have one recipe named `example`).

## configure kernel

It is best to run menuconfig from bitbake:

```shell
bitbake <target>:do_menuconfig
```

If you made any changes and saved, you can use:

```shell
bitbake <target>:do_diffconfig
```

You will get a message telling you where the `.cfg` file has been output to. Then, copy this to the files folder of your target recipe and add it in the `SRC_URI`.

The same `.cfg` file can be obtained from Linux kernel repository by typing the following in the kernel folder:

```shell
scripts/diffconfig -m <oldconf> <newconf> > fragment.cfg
```

## add kernel module

In our example, we will call our first module as `hello-mod`. Depending on the layer you want to use, you should create the `hello-mod` folder inside the `recipes-kernel` directory. There, in `recipes-kernel/hello-mod`, create a file called `hello-mod_0.1.bb` and a folder named `files`.

In `files` folder, put `hello.c` and `Makefile` (you can use the same from [hello world module](#hello-world-module)). You will also need a licence file which you can obtain from https://www.gnu.org/licenses/. Call it `COPYING` and get its checksum by using:

```shell
$ md5sum COPYING
```

After this, fill out the `hello-mod_0.1.bb` with following:

```shell
SUMMARY = "My first kernel module in Yocto"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e"

inherit module

SRC_URI = "file://Makefile"
SRC_URI += "file://hello-mod.c"
SRC_URI += "file://COPYING"

S = "${WORKDIR}"

RPROVIDES_${PN} += "kernel-module-hello-mod"
```

Then, in bitbake shell, you can see if everything went OK:

```shell
$ bitbake-layers show-recipes | grep hello-mod -A 1
```

You should see your kernel module, and below its name the name of the layer it resides in. Then, you can try building it:

```shell
$ bitbake hello-mod
```

If there are any error messages, handle them accordingly.

Once built, you can copy it to the target system and run with `sudo insmod <path_to_hello-mod.ko>`. Note that kernel versions have to match: `vermagic.o` is linked against the module to check this.


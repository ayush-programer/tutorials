# Linux Kernel Hacking

Note: Just for convenience, link references to kernel source code will be for version `5.0`.

## Kernel Source Folder Structure

### `arch/`

architecture specific code:

+ low memory management
+ interrupt handling
+ early initialization

### `crypto/`

cryptographic API used by kernel itself

### `drivers/`

code to run peripheral devices:

+ video
+ low-level SCSI

#### `drivers/net`

network card drivers

### `fs/`

+ generic filesystem code (Virtual File System)
+ code for each different filesystem (e.g. `ext2`)

### `include/`

header files

#### `include/asm-<arch>/`

architecture specific header files

### `init/`

code for creating early userspace and:

+ `main.c`
+ `version.c` - defines Linux version string

### `ipc/`

Inter Process Communication:

+ shared memory
+ semaphores

### `kernel/`

generic kernel level code:

+ upper level system call
+ printk()
+ scheduler
+ signal handling

### `lib/`

routines of generic usefulness

+ common string operations
+ debugging routines
+ line parsing

### `mm/`

high level memory management code with:

+ early boot memory management
+ memory mapping of files
+ management of page caches
+ memory allocation
+ swap out of pages in RAM

### `net/`

high-level networking code (low-level network drivers pass packets here)

#### `net/core/`

code for most of different network protocols

### `scripts/`

scripts useful in building the kernel

### `security/`

code for different Linux security models

### `sound/`

drivers for sounds cards etc.

### `usr/`

code that builds a cpio-format archive containing a root filesystem image

## Kernel version

To get kernel version, you can use the `LINUX_VERSION_CODE` macro. You can compare that against target kernel version (assume it is `v4.15.0`) that can be obtained in proper format by using `KERNEL_VERSION(4,15,0)`.

To get version information at runtime, use:

```c
char *kernel_version = utsname()->release;
```

Note: For the former method include `linux/version.h` and for the latter `linux/utsname.h`.

### Preemption info

Short summary of low latency and RT kernel versions can be found [here](https://elixir.bootlin.com/linux/latest/source/kernel/Kconfig.preempt).

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

Note: An alternative to `printk` is:

```c
seq_printf("struct seq_file *sfile, const char *fmt, ...);
```

This function will write to a specified file instead of `dmesg`. It is imported from `linux/seq_file.h`. See tutorial on `seq_file` [here](#the-seq-file).

### Log level

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

### Rate limit of printk

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

## Configuration

To configure the kernel, run:

```shell
make menuconfig
```

Note: It's best to do kernel configuration via the Yocto build system.

### Expose configuration file

To expose the kernel configuration file in `/proc/config.gz`, the following two options in kernel configuration should be considered:

```
CONFIG_IKCONFIG
CONFIG_IKCONFIG_PROC
```

## Processes

You can iterate over process list:

```c
struct task_struct *g, *p;

read_lock(&tasklist_lock);
for_each_process_thread(g, p) {
	/* operate on p */
}
read_unlock(&tasklist_lock);
```

Note: You can find definition of `task_struct` in `linux/sched.h`, specifically [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/sched.h#L592). This struct is initialized statically in `init/init_task.c`, and can be found [here](https://elixir.bootlin.com/linux/v5.0/source/init/init_task.c#L57).

## CPUs

You can iterate over CPUs with one of macros defined [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/cpumask.h#L777):

```c
#define for_each_possible_cpu(cpu) for_each_cpu((cpu), cpu_possible_mask)
#define for_each_online_cpu(cpu)   for_each_cpu((cpu), cpu_online_mask)
#define for_each_present_cpu(cpu)  for_each_cpu((cpu), cpu_present_mask)
```

Note: `for_each_online_cpu()` should be used within a `get_online_cpus()` and `put_online_cpus()` section, to prevent the online CPU map changing during iteration.

Note: You can also find out if CPU is online with `cpu_online(cpu)`.

### Current CPU

To get current CPU id, use `smp_processor_id()`. Be careful, however, as preemption has to be disabled before using it with `preempt_disable()` (and later reenabled with `preempt_enable()`).

### Per-CPU variables

To use per-cpu variables, first include `linux/percpu.h`.

#### Define and declare

You can define a per-cpu variable using the following macro:

```c
DEFINE_PER_CPU(type, name);
```

Similarly, you can declare it by using:

```c
DECLARE_PER_CPU(type, name);
```

Note: Per-CPU variables can also be exported.

#### Assign and get value

To get from or assign a value to a per-cpu variable, use:

```c
per_cpu(variable, cpu)
```

This can be used also as an `lvalue`, so you can type:

```c
per_cpu(variable, cpu) = 0;
```

#### Per-CPU section

Preemption usually has to be disabled when dealing with per-CPU variables; for that, you can use:

* `get_cpu_var(variable)` - value can be modified, and preemption is disabled
* `put_cpu_var(variable)` - end of variable usage, preemption is enabled

Note: You can find out more on per-CPU variables [here](https://lwn.net/Articles/22911/).

## Atomics

Find out more about atomics [here](https://www.infradead.org/~mchehab/kernel_docs/core-api/atomic_ops.html).

## Permissions

For `umode_t`, the values from `linux/stat.h` (found [here](https://elixir.bootlin.com/linux/latest/source/include/linux/stat.h)):

```c
#define S_IRWXUGO	(S_IRWXU|S_IRWXG|S_IRWXO)
#define S_IALLUGO	(S_ISUID|S_ISGID|S_ISVTX|S_IRWXUGO)
#define S_IRUGO		(S_IRUSR|S_IRGRP|S_IROTH)
#define S_IWUGO		(S_IWUSR|S_IWGRP|S_IWOTH)
#define S_IXUGO		(S_IXUSR|S_IXGRP|S_IXOTH)
```

You can find the rest of the definitions in `linux/uapi/stat.h` on this [link](https://elixir.bootlin.com/linux/latest/source/include/uapi/linux/stat.h). The list is here:

```c
#define S_IRWXU 00700
#define S_IRUSR 00400
#define S_IWUSR 00200
#define S_IXUSR 00100

#define S_IRWXG 00070
#define S_IRGRP 00040
#define S_IWGRP 00020
#define S_IXGRP 00010

#define S_IRWXO 00007
#define S_IROTH 00004
#define S_IWOTH 00002
#define S_IXOTH 00001
```

These values correspond to user, group and other privilege levels (read/write/execute).

## seq file

First, you have to conform to these function pointers (as defined [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/seq_file.h#L32)):

```c
void *(*start) (struct seq_file *m, loff_t *pos);
void (*stop) (struct seq_file *m, void *v);
void *(*next) (struct seq_file *m, void *v, loff_t *pos);
int (*show) (struct seq_file *m, void *v);
```

The handlers should be loaded in `struct seq_operations` which will be used to create a wrapper for `open`:

```c
static int seqf_ex_proc_open(struct inode* inode, struct file* file)
{
	return seq_open(file, &seqf_ex_ops);
}
```

All that is left is to create a `struct file_operations` that you can use:

```c
static struct file_operations seqf_ex_proc_ops = {
	.owner		= THIS_MODULE,
	.open		= seqf_ex_proc_open,
	.read		= seq_read,
	.llseek		= seq_lseek,
	.release	= seq_release
};
```

Note: The functions `seq_read`, `seq_lseek` and `seq_release` are defined in the kernel itself (no need to write them yourself).

See the `seqf-ex` folder for a simple introductory example.

## procfs

The proc filesystem is exposed via the `/proc` folder. Using debug filesystem is a better alternative in modern kernel programming.

Note: To use in kernel development, include `linux/proc_fs.h`.

### Create file

To create a file in the procfs, you can use the following function:

```c
struct proc_dir_entry *proc_create(const char *name, umode_t mode,
				   struct proc_dir_entry *parent,
				   const struct file_operations *proc_fops);
```

### Create folder

To create a subfolder in the proc filesystem, use:

```
struct proc_dir_entry* proc_mkdir(const char *name,
				  struct proc_dir_entry *parent)
```

### Remove entry

To remove the file, or folder, use:

```c
void remove_proc_entry(const char *name, struct proc_dir_entry *parent);
```

Note: Example usage of proc filesystem can be found in the `seqfs-ex` example.

## debugfs

The debug filesystem is usually mounted to `/sys/kernel/debug`. You can mount it manually, if necessary:

```shell
mount -t debugfs none /sys/kernel/debug/
```

Note: For use in kernel include `linux/debugfs.h` header file.

### Create file

To create a file in the debugfs, use:

```c
struct dentry *debugfs_create_file(const char *name, umode_t mode,
				   struct dentry *parent, void *data,
				   const struct file_operations *fops);
```

### Create folder

To create a subfolder in the debug filesystem, use:

```c
struct dentry *debugfs_create_dir(const char *name,
				  struct dentry *parent);
```

### Remove entry

To remove an entry, use:

```
void debugfs_remove(struct dentry *dentry);
```

Note: Example usage of debugfs can be found in `relay-ex` example.

## Relay channel

You can find out more about the relay channel [here](http://relayfs.sourceforge.net/relayfs.txt). Also, include `linux/relay.h` header file.

These are the two most important handlers:

```c
struct dentry* create(const char* filename, struct dentry* parent,
		      umode_t mode, struct rchan_buf* buf,
		      int* is_global);
int delete(struct dentry *dentry);
```

Load them into the `struct rchan_callback`; definition can be found [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/relay.h#L80).

These callbacks can then be loaded in:

```c
struct rchan *relay_open(const char *base_filename,
			 struct dentry *parent,
			 size_t subbuf_size,
			 size_t n_subbufs,
			 struct rchan_callbacks *cb,
			 void *private_data);
```

To write data to a relay channel, use:

```c
void relay_write(struct rchan *chan, const void *data, size_t length);
```

Closing the relay channel is simple:

```c
relay_close(struct rchan* rchan);
```

Note: See the `relay-ex` for a simple relay channel example.

## Current process

Pointer to the `task struct` of the current process is `current`; so mostly anywhere in the kernel code, you can write things such as:

```c
printk(KERN_INFO "%s, %d", current->comm, current->pid);
```

Note: This is imported from `linux/sched.h`.

## Container of a variable

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

## Exporting symbols

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

## User-space and kernel-space

### Compiler information

In `C`, you can easily distinguish whether your code is run in kernel-space or user-space context with `__KERNEL__` macro:

```c
#ifdef __KERNEL__
	/* code for kernel-space */
#else
	/* code for user-space */
```

### Data exchange

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

## Synchronization

### Semaphores / Mutexes

Semaphores are defined in `linux/semaphore.h`.

#### Initialization

To initialize, use:

```c
void sema_init(struct semaphore *sem, int val);
```

To initialize semaphore as a mutex at compile time, use:

```c
DECLARE_MUTEX(name);
DECLARE_MUTEX_LOCKED(name);
```

To initialize a mutex at runtime:

```c
void init_MUTEX(struct semaphore *sem);
void init_MUTEX_LOCKED(struct semaphore *sem);
```

#### Locking

Each of the following functions takes `struct semaphore*` as an argument:

|       function       |                description               | ret  |
|----------------------|------------------------------------------|------|
|        `down`        | decrement / acquire lock                 | void |
| `down_interruptible` | like `down`, but can be interrupted      | int  |
|   `down_killable`    | like `down`, but process can be killed   | int  |
|    `down_trylock`    | returns with non-zero value on lock fail | int  |
|         `up`         | increment / release lock                 | void |

Note: Common pattern with `down_interruptible` in device drivers is to return `-ERESTARTSYS` (to restart the call) or `-EINTR` (if restarting is impossible).

### Reader/Writer Semaphores

Include `linux/rwsem.h`.

#### Initialization

To initialize the `rwsem`, use:

```c
void init_rwsem(struct rw_semaphore* sem);
```

#### Locking

All of the following functions take `struct rw_semaphore*` as argument:

|       function       |               description          | ret  |
|----------------------|------------------------------------|------|
|      `down_read`     | reader lock                        | void |
| `down_read_trylock`  | return non-zero on read lock fail  | int  |
|       `up_read`      | reader unlock                      | void |
|     `down_write`     | writer lock                        | void |
| `down_write_trylock` | return non-zero on write lock fail | int  |
|       `up_write`     | writer unlock                      | void |
|  `downgrade_write`   | allow other readers after write    | void |

### Spinlocks

### Completion

Include `linux/completion.h` then define and initialize:

```c
struct completion my_completion;

init_completion(&my_completion);
```

Then, to wait for completion:

```c
wait_for_completion(&my_completion);
```

To signal completion:

```c
complete(&my_completion);
```

## Linked lists

### Definition

This is a definition of `list_head` (include it from `linux/types.h`):

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

### Initialization

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

### Add an element

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

### Iterate over list

```c
struct list_head *ptr;
struct node_el *entry;

list_for_each(ptr, &my_list) {
	entry = list_entry(ptr, struct node_el, list1);
}
```

### Deinitialize

To delete an element from the list:

```c
list_del(ptr);
```

To delete the whole list, just iterate over the list deleting nodes (use the safe variant, though):

```c
struct list_head *ptr;
struct list_head *tmp
struct node_el *entry;

list_for_each_safe(ptr, tmp, &my_list) {
	list_del(ptr);
}
```

### High Resolution Timer

First, include `linux/hrtimer.h`.

#### Initialization

To initialize `hrtimer`, use:

```c
void hrtimer_init(struct hrtimer *timer, clockid_t which_clock,
		  enum hrtimer_mode mode);
```

Values for `which_clock` are defined [here](https://elixir.bootlin.com/linux/v5.0/source/include/uapi/linux/time.h#L71) as:

```c
#define CLOCK_REALTIME			0
#define CLOCK_MONOTONIC			1
#define CLOCK_PROCESS_CPUTIME_ID	2
#define CLOCK_THREAD_CPUTIME_ID		3
#define CLOCK_MONOTONIC_RAW		4
#define CLOCK_REALTIME_COARSE		5
#define CLOCK_MONOTONIC_COARSE		6
#define CLOCK_BOOTTIME			7
#define CLOCK_REALTIME_ALARM		8
#define CLOCK_BOOTTIME_ALARM		9
```

You can find options for `hrtimer_mode` [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/hrtimer.h#L26). The following can be combined (with only `ABS` and `REL` being mutually exclusive):

```c
/*
 * Mode arguments of xxx_hrtimer functions:
 *
 * HRTIMER_MODE_ABS		- Time value is absolute
 * HRTIMER_MODE_REL		- Time value is relative to now
 * HRTIMER_MODE_PINNED		- Timer is bound to CPU (is only considered
 *				  when starting the timer)
 * HRTIMER_MODE_SOFT		- Timer callback function will be executed in
 *				  soft irq context
 */
```

#### Set the callback

Once `struct hrtimer* my_timer` has been initialized, define the callback as:

```c
enum hrtimer_restart timer_callback(struct hrtimer *timer)
```

The return value can be found [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/hrtimer.h#L53), defined as:

```c
enum hrtimer_restart {
	HRTIMER_NORESTART,	/* Timer is not restarted */
	HRTIMER_RESTART,	/* Timer must be restarted */
};
```

Note: In case of `HRTIMER_RESTART`, forward the hrtimer expiry by using the function (defined [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/hrtimer.h#L451):

```c
static inline u64 hrtimer_forward_now(struct hrtimer *timer,
				      ktime_t interval)
```

Then, simply add the callback to the `struct hrtimer* my_timer` by using:

```c
my_timer.function = timer_callback;
```

#### Start hrtimer

To start the `hrtimer`, use the following function (defined [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/hrtimer.h#L384)):

```c
/**
 * hrtimer_start - (re)start an hrtimer
 * @timer:	the timer to be added
 * @tim:	expiry time
 * @mode:	timer mode: absolute (HRTIMER_MODE_ABS) or
 *		relative (HRTIMER_MODE_REL), and pinned (HRTIMER_MODE_PINNED);
 *		softirq based mode is considered for debug purpose only!
 */
static inline void hrtimer_start(struct hrtimer *timer, ktime_t tim,
				 const enum hrtimer_mode mode)
```

For `ktime_t` argument, include `linux/ktime.h` and use:

```c
static inline ktime_t ktime_set(const s64 secs, const unsigned long nsecs)
```

This function is defined [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/ktime.h#L30).

#### Cancel

To cancel the timer, use:

```c
int hrtimer_cancel(struct hrtimer *timer);
```

## Kernel modules

### Commands and info

|    comm    |        meaning       |
|------------|----------------------|
| `lsmod`    | list kernel modules  |
| `insmod`   | insert kernel module |
| `rmmod`    | remove kernel module |

Note: The `modprobe` command is the same as `insmod` but it also inserts any kernel modules on which the current one depends. In other words, it might work when `insmod` does not.

To get information on currently loaded modules:

```shell
cat /proc/modules
```

List of kernel modules to be loaded at boot-time:

```shell
cat /etc/modules
```

### "Hello world" module

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

### Char driver

#### Major and minor numbers

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

#### File operations

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

Note: You can find the full list of `struct file_operations` function pointers [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/fs.h#L1783).

Note: For `llseek` implementation, check out macros defined [here](https://elixir.bootlin.com/linux/v5.0/source/include/uapi/linux/fs.h#L40).

#### The file structure

You can find the reference on `struct file` [here](https://elixir.bootlin.com/linux/v5.0/source/include/linux/fs.h#L901).

## Add command to `sysctl`

You can add new commands to `sysctl` for kernel fine-tuning. In the kernel repo, open the `kernel/sysctl.c` file. There, you will see a list of `sysctl` options, so copying one of them and appending it is the way to go. For example, add this to the end of `kern_table[]` in `sysctl.c`:

```c
{
	.procname	= "example_control",
	.data		= &example_control,
	.maxlen		= sizeof(int),
	.mode		= 0644,
	.proc_handler	= proc_dointvec_minmax,
	.extra1		= &zero,
	.extra2		= &one,
}
```

Then, declare `example_control` variable in `include/linux/sysctl.h` as `extern`:

```c
extern int example_control;
```

Finally, in the file you are going to use this variable, declare and initialize:

```c
int __read_mostly example_control = 0;
```

Note: The `__read_mostly` keyword only tells the compiler it will rarely be written (and more often read).

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

# RCU Subsystem

Find out about RCU subsystem [here](https://lwn.net/Articles/262464/). You can get information on debugging RCU stalls and other issues [here](https://www.kernel.org/doc/Documentation/RCU/stallwarn.txt).

# Kernel fine-tuning

Most of the parameters described here can be tweaked via `sysctl` or in `/proc/sys/kernel/` folder.

## Dirty ratio



## Real-time group scheduling

Information on this topic in detail can be found [here](https://www.kernel.org/doc/Documentation/scheduler/sched-rt-group.txt).

* `sched_rt_period_us` - defines how long one real-time period lasts in microseconds
* `sched_rt_runtime_us` - defines how much microseconds can a real-time process take from a real-time period defined in the former variable

For example, if real-time period is 1000000us (1s) and real-time runtime is 950000us (0.95s), then, if a real-time process takes 0.95s of time in a second, RT throttling will be activated, and lower priority tasks will be allowed to run (taking the remaining 0.05s).

This can be further customized via cgroups (`CONFIG_RT_GROUP_SCHED` must be enabled).

## Round Robin

One can also specify how much time can a `SCHED_RR` task take in milliseconds via `sched_rr_timeslice_ms` variable.

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

## lockdep

Lockdep is used for deadlock detection in the kernel code. To enable it, run `menuconfig` and enable following features:

```
 1. [*] Detect Hard and Soft Lockups
 2. [*] Detect Hung Tasks
 3. [*] RT Mutex debugging, deadlock detection
 4. -*- Spinlock and rw-lock debugging: basic checks
 5. -*- Mutex debugging: basic checks
 6. -*- Lock debugging: detect incorrect freeing of live locks
 7. [*] Lock debugging: prove locking correctness
 8. [*] Lock usage statistics
```

After recompiling the kernel, you should see the following new folders:

```
/proc/lockdep
/proc/lockdep_chains
/proc/lockdep_stat
/proc/locks
/proc/lock_stats
```

If you are running a kernel module or driver via a specific application you can use:

```shell
ps -e -o comm,stat | grep <app_name>
```

If you see a `+D` (uninterruptible sleep) state, run `dmesg` to see lockdep printouts.

Note: You can read more about lockdep [here](https://www.kernel.org/doc/Documentation/locking/lockdep-design.txt).

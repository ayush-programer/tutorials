#include <linux/module.h>
#include <linux/kernel.h> // printk
#include <linux/fs.h> // semaphore and all about fs
#include <linux/cdev.h>
#include <linux/slab.h> // kmalloc
#include <linux/uaccess.h> // copy_from_user

static int simple_major = 0;
static int device_num = 1;

struct char_dev {
//	struct list_head memlist_head;
	struct semaphore sem;
	struct cdev cdev;
	char *data;
};

/*
static struct mem_chunk {
	struct list_head lhead;
	char data[MAX_PER_NODE];
	int last;
};
*/

static struct char_dev *char_devices;

static int char_drv_open(struct inode *inode, struct file *filp)
{
	struct char_dev* char_drv_dev;

	pr_err("char-drv: open\n");

	char_drv_dev = container_of(inode->i_cdev, struct char_dev, cdev);

	filp->private_data = (void*)char_drv_dev;

	return 0;
}

static int char_drv_release(struct inode* inode, struct file* filp)
{
	pr_err("char-drv: release\n");

	return 0;
}

static ssize_t char_drv_read(struct file* filp, char* buff, size_t size, loff_t* loff)
{
	static int read_count = 0;
	char kbuffer[8] = "nothing\n";

	if (read_count) {
		read_count = 0;
		return 0;
	}

	if (copy_to_user(buff, kbuffer, 8)) return -ENOMEM;

	pr_err("char-drv: read\n");

	read_count++;

	return 8;
}

static ssize_t char_drv_write(struct file* filp, const char* buff, size_t size, loff_t* loff)
{
	char kbuffer[256] = { 0 };

	if (size > 256)
		return -ENOMEM;

	if (copy_from_user(kbuffer, buff, size))
		return -ENOMEM;

	pr_err("char-drv: writing: %s\n", kbuffer);

	return size;
}

static struct file_operations char_fops = {
	.owner		= THIS_MODULE,
	.open		= char_drv_open,
	.release	= char_drv_release,
	.read		= char_drv_read,
	.write		= char_drv_write,
};

static void setup_char_drv(struct cdev *cdev, int minor)
{
	int err;
	int dev = MKDEV(simple_major, minor);

	cdev_init(cdev, &char_fops);
	cdev->owner = THIS_MODULE;
	cdev->ops = &char_fops;

	/* cdev_add(
	 *	struct cdev *dev,
	 *	dev_t num,
	 *	unsigned int count	<- usually 1, except in special cases
	 * ) */
	err = cdev_add(cdev, dev, 1);

	if (err) {
		pr_err("char-drv: Failed adding char-drv.\n");
		return;
	}
}

// module entrypoint
static int __init char_drv_start(void)
{
	int result;
	dev_t dev;
	int i;

	pr_err("char-drv: starting driver...\n");

	if (device_num <= 0) {
		pr_err("char-drv: device_num parameter has to be larger than zero.\n");
		return -1;
	}

	char_devices = kmalloc(sizeof(*char_devices) * device_num, GFP_KERNEL | GFP_NOWAIT);

	if (simple_major) {
		// if simple_major is not 0, create dev, and register it
		dev = MKDEV(simple_major, 0);
		result = register_chrdev_region(dev, device_num, "char-drv");
	}
	else {
		// if simple_major is 0, then ask the system to give us dev
		result = alloc_chrdev_region(&dev, 0, device_num, "char-drv");
	}

	if (result < 0) {
		pr_err("chr_drv: unable to get major %d\n", simple_major);
		return result;
	}

	simple_major = MAJOR(dev);

	for (i = 0; i < device_num; i++)
		setup_char_drv(&char_devices[i].cdev, i);

	return 0;
}

static void __exit char_drv_end(void)
{
	int i;

	pr_err("char-drv: closing driver...\n");

	for (i = 0; i < device_num; i++)
		cdev_del(&char_devices[i].cdev);

	kfree(char_devices);

	unregister_chrdev_region(MKDEV(simple_major, 0), device_num);
}

module_param(simple_major, int, 0);
module_param(device_num, int, 0);
module_init(char_drv_start);
module_exit(char_drv_end);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("simple char driver example");
MODULE_VERSION("0.1");

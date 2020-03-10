#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/types.h>

#define MAX_PER_NODE 2048

static int simple_major = 0;
static int device_num = 1;

struct char_dev {
	struct list_head mem_chunk_list;
	struct semaphore sem;
	struct cdev cdev;
};

struct mem_chunk {
	struct list_head lhead;
	char* data;
	int last;
};

static struct char_dev *char_devices;

static int char_drv_open(struct inode *inode, struct file *filp)
{
	struct char_dev* char_drv_dev;

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

	if (copy_to_user(buff, kbuffer, 8))
		return -ENOMEM;

	read_count++;

	return 8;
}

static ssize_t char_drv_write(struct file* filp, const char* buff, size_t size, loff_t* loff)
{
	int size_to_be_written;
	struct char_dev* char_drv_dev;
	struct list_head *ptr;
	struct node_el *entry;
	struct mem_chunk *new_el;

	size_to_be_written = (size > MAX_PER_NODE) ? MAX_PER_NODE : size;
 	char_drv_dev = (struct char_dev*)filp->private_data;

	if(list_empty(&char_drv_dev->mem_chunk_list)) {
		new_el = kmalloc(sizeof(*new_el), GFP_KERNEL);
		new_el->data = kmalloc(MAX_PER_NODE, GFP_KERNEL);
		list_add(&new_el->lhead, &char_drv_dev->mem_chunk_list);
		return 0;
	}
	else {

	}
/*
	list_last_entry

	list_for_each(ptr, &my_list) {
		entry = list_entry(ptr, struct node_el, list1);
	}

	if (copy_from_user(kbuffer, buff, size))
		return -ENOMEM;
*/
	return size_to_be_written;
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
	struct char_dev* char_drv_dev;

	cdev_init(cdev, &char_fops);
	cdev->owner = THIS_MODULE;
	cdev->ops = &char_fops;

	err = cdev_add(cdev, dev, 1);

	if (err) {
		pr_err("char-drv-ll: Failed adding char-drv.\n");
		return;
	}

	char_drv_dev = container_of(cdev, struct char_dev, cdev);

	INIT_LIST_HEAD(&char_drv_dev->mem_chunk_list);

	return;
}

static int __init char_drv_start(void)
{
	int result;
	dev_t dev;
	int i;

	if (device_num <= 0) {
		pr_err("char-drv-ll: device_num parameter has to be larger than zero.\n");
		return -1;
	}

	char_devices = kmalloc(sizeof(*char_devices) * device_num, GFP_KERNEL | GFP_NOWAIT);

	if (simple_major) {
		dev = MKDEV(simple_major, 0);
		result = register_chrdev_region(dev, device_num, "char-drv");
	}
	else {
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
MODULE_DESCRIPTION("Simple char driver and linked list example");
MODULE_VERSION("0.1");

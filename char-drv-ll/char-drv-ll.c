#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/cdev.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/types.h>

#define MAX_PER_NODE 16

static int simple_major = 0;
static int device_num = 1;

struct char_dev {
	struct list_head mem_chunk_list;
	struct semaphore sem;
	long size;
	struct cdev cdev;
};

struct mem_chunk {
	struct list_head lhead;
	char* data;
};

static struct char_dev *char_devices;

static int char_drv_open(struct inode *inode, struct file *filp)
{
	struct char_dev* char_drv_dev;

	char_drv_dev = container_of(inode->i_cdev, struct char_dev, cdev);

	down_interruptible(&char_drv_dev->sem);
	filp->private_data = (void*)char_drv_dev;
	up(&char_drv_dev->sem);

	return 0;
}

static int char_drv_release(struct inode* inode, struct file* filp)
{
	return 0;
}

static ssize_t char_drv_read(struct file* filp, char* buff,
			     size_t size, loff_t* loff)
{
	int list_item;
	int loff_remainder;
	struct char_dev* char_drv_dev;
	struct list_head* ptr;
	struct mem_chunk* entry;
	int remaining_bytes;
	int size_to_be_read;
	long partial_size;

	char_drv_dev = (struct char_dev*)filp->private_data;

	down_interruptible(&char_drv_dev->sem);

	size_to_be_read = 0;

	if (char_drv_dev->size < *loff) {
		pr_err("char-drv-ll: Invalid offset: %ld\n", (long)*loff);
		size_to_be_read = -ENXIO;
		goto end_read;
	}
	else if (char_drv_dev->size == *loff) {
		goto end_read;
	}

	partial_size = (int)(char_drv_dev->size -
		       (char_drv_dev->size % MAX_PER_NODE));
	list_item = (int)((long)*loff / MAX_PER_NODE);
	loff_remainder = (int)((long)*loff % MAX_PER_NODE);

	list_for_each(ptr, &char_drv_dev->mem_chunk_list) {
		entry = list_entry(ptr, struct mem_chunk, lhead);

		if (list_item-- != 0) {
			continue;
		}

		entry = list_entry(ptr, struct mem_chunk, lhead);
		remaining_bytes = partial_size > *loff
				? MAX_PER_NODE
				: char_drv_dev->size - *loff;

		if (remaining_bytes <= 0) {
			size_to_be_read = 0;
			goto end_read;
		}

		size_to_be_read = remaining_bytes < size
				? remaining_bytes
				: size;

		if (copy_to_user(buff, &(entry->data[loff_remainder]),
				 size_to_be_read)) {
			size_to_be_read = -ENOMEM;
			goto end_read;
		}

		*loff += size_to_be_read;

		goto end_read;
	}

end_read:
	up(&char_drv_dev->sem);

	return size_to_be_read;
}

static ssize_t char_drv_write(struct file* filp, const char* buff,
			      size_t size, loff_t* loff)
{
	int size_to_be_written;
	struct char_dev* char_drv_dev;
	struct list_head* ptr;
	struct mem_chunk* entry;
	struct mem_chunk* new_el;
	int remaining_bytes;
	int list_item;
	int loff_remainder;
	long new_size;

 	char_drv_dev = (struct char_dev*)filp->private_data;

	down_interruptible(&char_drv_dev->sem);

	if (char_drv_dev->size < *loff) {
		pr_err("char-drv-ll: Invalid offset: %ld\n", (long)*loff);
		size_to_be_written = -ENXIO;
		goto end_write;
	}

	list_item = (int)((long)*loff / MAX_PER_NODE);
	loff_remainder = (int)((long)*loff % MAX_PER_NODE);

	list_for_each(ptr, &char_drv_dev->mem_chunk_list) {

		if (list_item-- != 0) {
			continue;
		}

		entry = list_entry(ptr, struct mem_chunk, lhead);
		remaining_bytes = MAX_PER_NODE - loff_remainder;

		if (remaining_bytes <= 0) {
			break;
		}

		size_to_be_written = remaining_bytes < size
				   ? remaining_bytes
				   : size;

		if (copy_from_user(&(entry->data[loff_remainder]), buff,
				     size_to_be_written)) {
			size_to_be_written = -ENOMEM;
			goto end_write;
		}

		new_size = (long)*loff + size;

		if (new_size > char_drv_dev->size) {
			char_drv_dev->size = new_size;
		}

		*loff += size_to_be_written;

		goto end_write;
	}

	new_el = kmalloc(sizeof(*new_el), GFP_KERNEL);
	new_el->data = kmalloc(MAX_PER_NODE, GFP_KERNEL);
	size_to_be_written = size >= MAX_PER_NODE ? MAX_PER_NODE : size;

	*loff += size_to_be_written;

	if (copy_from_user(new_el->data, buff, size_to_be_written)) {
		size_to_be_written = -ENOMEM;
		goto end_write;
	}

	list_add_tail(&new_el->lhead, &char_drv_dev->mem_chunk_list);

	char_drv_dev->size += size_to_be_written;

end_write:

	up(&char_drv_dev->sem);

	return size_to_be_written;
}

static loff_t char_drv_llseek (struct file *filp, loff_t loff, int whence)
{
	struct char_dev* char_drv_dev;

	char_drv_dev = (struct char_dev*)filp->private_data;

	switch (whence) {
		case SEEK_SET:
			return loff;
		case SEEK_CUR:
			return filp->f_pos + loff;
		case SEEK_END:
			return char_drv_dev->size + loff;

	}

	return -EINVAL;
}

static struct file_operations char_fops = {
	.owner		= THIS_MODULE,
	.open		= char_drv_open,
	.release	= char_drv_release,
	.read		= char_drv_read,
	.write		= char_drv_write,
	.llseek		= char_drv_llseek
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
	char_drv_dev->size = 0;
	sema_init(&char_drv_dev->sem, 1);

	return;
}

static int __init char_drv_start(void)
{
	int result;
	dev_t dev;
	int i;

	if (device_num <= 0) {
		pr_err("char-drv-ll: Parameter device_num "
			"has to be larger than zero.\n");
		return -1;
	}

	char_devices = kmalloc(sizeof(*char_devices) * device_num,
			       GFP_KERNEL | GFP_NOWAIT);

	if (simple_major) {
		dev = MKDEV(simple_major, 0);
		result = register_chrdev_region(dev, device_num, "char-drv-ll");
	}
	else {
		result = alloc_chrdev_region(&dev, 0, device_num, "char-drv-ll");
	}

	if (result < 0) {
		pr_err("chr_drv-ll: Unable to get major %d\n", simple_major);
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
	struct list_head* ptr;
	struct list_head* tmp;
	struct mem_chunk* entry;
	struct char_dev* char_drv_dev;

	for (i = 0; i < device_num; i++) {
		char_drv_dev = container_of(&char_devices[i].cdev,
				struct char_dev, cdev);

		down_interruptible(&char_drv_dev->sem);

		list_for_each_safe(ptr, tmp, &char_drv_dev->mem_chunk_list) {
			entry = list_entry(ptr, struct mem_chunk, lhead);
			kfree(entry->data);
			list_del(ptr);
		}

		cdev_del(&char_devices[i].cdev);

		up(&char_drv_dev->sem);
	}

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

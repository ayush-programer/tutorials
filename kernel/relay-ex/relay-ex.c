#include <linux/module.h>
#include <linux/debugfs.h>
#include <linux/relay.h>
#include <linux/version.h>

#define SUB_BUFFER_SIZE 2048
#define SUB_BUFFER_NUM 4

static char buffer[SUB_BUFFER_SIZE] = { 0 };
static struct rchan* channel;

/* the /proc entry open procedures */

static struct dentry* relay_ex_dir;

static int relay_ex_subbuf_start(struct rchan_buf *buf,
				 void *subbuf,
				 void *prev_subbuf,
				 size_t prev_padding)
{
	if (relay_buf_full(buf)) {
		pr_err("cpu %d buffer full!!!\n", smp_processor_id());
		return 0;
	}

	return 1;
}

static struct dentry* relay_ex_create_f(const char* filename,
					struct dentry* parent,
					umode_t mode,
					struct rchan_buf* buf,
					int* is_global)
{
	struct dentry* relay_ex_entry;

	relay_ex_entry = debugfs_create_file(filename, mode,
					     relay_ex_dir, buf,
					     &relay_file_operations);

	return relay_ex_entry;
}

static int relay_ex_delete_f(struct dentry *dentry)
{
	debugfs_remove(dentry);

	return 0;
}

static struct rchan_callbacks relay_callbacks =
{
	.subbuf_start = relay_ex_subbuf_start,
	.create_buf_file = relay_ex_create_f,
	.remove_buf_file = relay_ex_delete_f,
};

static int __init relay_ex_init(void)
{
	char* data = "abcdefghijklmnopqrstuvwz";
	char* data_pointer = 0;
	int buffer_pos = 0;

	data_pointer = data;

	/* we will fill the buffer with data */

	while (buffer_pos < 2048) {
		data_pointer = (*data_pointer == '\0') ? data : data_pointer;
		buffer[buffer_pos++] = *data_pointer;
		data_pointer += 1;
	}

	/* create entry in /sys/kernel/debug folder */

	relay_ex_dir = debugfs_create_dir("relay-ex", NULL);

	if (!(channel = relay_open("cpu", relay_ex_dir, SUB_BUFFER_SIZE,
				   SUB_BUFFER_NUM, &relay_callbacks, NULL))) {

		pr_err("Relay channel create failed.\n");
		return -ENOENT;
	}

	relay_write(channel, &buffer, sizeof(buffer));

	return 0;
}

static void __exit relay_ex_exit(void)
{
	/* close relay channel */

	relay_close(channel);

	/* remove debugfs dir */

	debugfs_remove(relay_ex_dir);
}

module_init(relay_ex_init);
module_exit(relay_ex_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("Simple relay example.");
MODULE_VERSION("0.1");

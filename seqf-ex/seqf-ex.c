#include <linux/module.h>
#include <linux/seq_file.h>
#include <linux/proc_fs.h>
#include <linux/version.h>

#define BUFFER_SIZE 2048
#define BUFFER_STEP 128
#define BUFFER_CHUNKS BUFFER_SIZE / BUFFER_STEP

static char buffer[BUFFER_SIZE] = { 0 };

static void* seqf_ex_start (struct seq_file* m, loff_t* pos)
{
	loff_t check_pos = *pos * BUFFER_STEP;

	if (check_pos >= BUFFER_SIZE) {
		return NULL;
	}

	return buffer + check_pos;
}

static void seqf_ex_stop (struct seq_file* m, void* v)
{
	/* any cleanup code goes here */
}

static void* seqf_ex_next (struct seq_file* m, void* v, loff_t* pos)
{
	/* due to compatibility issues between 4.x and 5.x kernel
	 * versions, it's best to design the seq_file to increase
	 * the *pos value just by 1 */

	(*pos)++;

	return seqf_ex_start(m, pos);
}

static int seqf_ex_show (struct seq_file* m, void* v)
{
	seq_printf(m, "%.*s\n", BUFFER_STEP, (char*)v);

	return 0;
}

static struct seq_operations seqf_ex_ops = {
	.start	= seqf_ex_start,
	.next	= seqf_ex_next,
	.stop	= seqf_ex_stop,
	.show	= seqf_ex_show
};

/* the /proc entry open procedures */

static struct proc_dir_entry* proc_entry;

static int seqf_ex_proc_open(struct inode* inode, struct file* file)
{
	return seq_open(file, &seqf_ex_ops);
}

static struct file_operations seqf_ex_proc_ops = {
	.owner		= THIS_MODULE,
	.open		= seqf_ex_proc_open,
	.read		= seq_read,
	.llseek		= seq_lseek,
	.release	= seq_release
};

static int __init seqf_ex_init(void)
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

	/* create entry in /proc folder */

	proc_entry = proc_create("seqf-ex", 0644, NULL, &seqf_ex_proc_ops);

	return 0;
}

static void __exit seqf_ex_exit(void)
{
	/* remove entry from /proc */

	remove_proc_entry("seqf-ex", NULL);
}

module_init(seqf_ex_init);
module_exit(seqf_ex_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("Simple seq_file example.");
MODULE_VERSION("0.1");

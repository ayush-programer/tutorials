#include <linux/module.h>
#include <linux/seq_file.h>

void *seqf_ex_start (struct seq_file *m, loff_t *pos);
void seqf_ex_stop (struct seq_file *m, void *v);
void *seqf_ex_next (struct seq_file *m, void *v, loff_t *pos);
int seqf_ex_show (struct seq_file *m, void *v);

static int __init seqf_ex_start(void)
{



	return 0;
}

static void __exit seqf_ex_end(void)
{

}

module_init(seqf_ex_start);
module_exit(seqf_ex_end);


#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/workqueue.h>

static struct workqueue_struct *wq = 0;

static void test_work(struct work_struct* data) {

	pr_err("ee-kwtest: Test kworker running.");

	return;
}

DECLARE_WORK(history_work, test_work);

static int __init ee_kwtest_start(void)
{
	if (!wq)
		wq = create_singlethread_workqueue("test_wq");

	pr_err("workqueue-ex: Creating work");

	queue_work(wq, &history_work);

	return 0;
}

static void __exit ee_kwtest_end(void)
{
	return;
}

module_init(ee_kwtest_start);
module_exit(ee_kwtest_end);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("Simple workqueue example.");
MODULE_VERSION("0.1");

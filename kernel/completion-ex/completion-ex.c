#include <linux/module.h>
#include <linux/hrtimer.h>
#include <linux/ktime.h>
#include <linux/completion.h>

static struct completion my_completion;
static struct hrtimer my_hrtimer;
ktime_t my_ktime;

// timer callback function
enum hrtimer_restart timer_callback(struct hrtimer *timer)
{
	printk(KERN_INFO "completion-ex: Will complete...\n");

	complete(&my_completion);

	return HRTIMER_NORESTART;
}

static int __init comp_start(void)
{
	printk(KERN_INFO "completion-ex: Module start...\n");

	init_completion(&my_completion);

	my_ktime = ktime_set(2, 5000000);

	hrtimer_init(&my_hrtimer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
	my_hrtimer.function = &timer_callback;
	hrtimer_start(&my_hrtimer, my_ktime, HRTIMER_MODE_REL);

	wait_for_completion(&my_completion);

	printk(KERN_INFO "completion-ex: Complete!\n");

	return 0;
}

static void __exit comp_end(void)
{
	hrtimer_cancel(&my_hrtimer);
}

module_init(comp_start);
module_exit(comp_end);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("Simple completion example");
MODULE_VERSION("0.1");

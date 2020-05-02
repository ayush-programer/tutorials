#include <linux/module.h>
#include <linux/hrtimer.h>
#include <linux/ktime.h>

static struct hrtimer my_hrtimer;
ktime_t my_ktime;

// timer callback function
enum hrtimer_restart timer_callback(struct hrtimer *timer)
{
	// code to run on timer expire

	pr_err("Hello!\n");

	// forward the timer expiry

	hrtimer_forward_now(timer, my_ktime);

	return HRTIMER_RESTART;
}

static int __init hrt_start(void)
{
	// ktime_set(sec, nsec); here it is 2.5 seconds
	my_ktime = ktime_set(2, 5000000);

	// hrtimer setup
	hrtimer_init(&my_hrtimer, CLOCK_MONOTONIC, HRTIMER_MODE_REL);
	my_hrtimer.function = &timer_callback;
	hrtimer_start(&my_hrtimer, my_ktime, HRTIMER_MODE_REL);

	return 0;
}

static void __exit hrt_end(void)
{
	hrtimer_cancel(&my_hrtimer);
}

module_init(hrt_start);
module_exit(hrt_end);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("Simple hrtimer example");
MODULE_VERSION("0.1");

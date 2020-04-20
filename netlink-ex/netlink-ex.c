#include <linux/module.h>
#include <linux/netlink.h>
#include <linux/skbuff.h>
#include <net/sock.h>

static struct sock *netlink_sock;

static void nl_input(struct sk_buff *skb)
{
	struct nlmsghdr *nl_message_header;

	nl_message_header = nlmsg_hdr(skb);

	pr_err("Got message: %s\n", (char*)nlmsg_data((struct nlmsghdr*)skb->data));
}

static struct netlink_kernel_cfg netlink_cfg = {
	.groups = 1,
        .input = nl_input,
};

static int __init netlink_start(void)
{
	pr_err("Starting netlink...\n");
	netlink_sock = netlink_kernel_create(&init_net,
					     NETLINK_USERSOCK,
					     &netlink_cfg);

	return 0;
}

static void __exit netlink_end(void)
{
	netlink_kernel_release(netlink_sock);
}

module_init(netlink_start);
module_exit(netlink_end);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Stjepan Poljak");
MODULE_DESCRIPTION("Simple netlink example");
MODULE_VERSION("0.1");

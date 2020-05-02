#include <sys/socket.h>
#include <linux/netlink.h>
#include <stdlib.h>
#include <string.h>	/* memset */
#include <unistd.h>	/* getpid */
#include <stdio.h>
#include <errno.h>

int main(int argv, char* argc[]) {

	int sock_fd;
	struct sockaddr_nl src_addr, dest_addr;
	struct nlmsghdr *nlh;
	struct iovec iov;
	struct msghdr msg;

	if ((sock_fd = socket(PF_NETLINK, SOCK_RAW, NETLINK_USERSOCK)) < 0) {
		return 1;
	}

	memset(&src_addr, 0, sizeof(src_addr));
	src_addr.nl_family = AF_NETLINK;
	src_addr.nl_pid = getpid();

	bind(sock_fd, (struct sockaddr*)&src_addr, sizeof(src_addr));

	memset(&dest_addr, 0, sizeof(dest_addr));
	dest_addr.nl_family = AF_NETLINK;
	dest_addr.nl_pid = 0;		/* kernel */
	dest_addr.nl_groups = 0;	/* unicast */

	nlh = (struct nlmsghdr *)malloc(NLMSG_SPACE(256));
	memset(nlh, 0, NLMSG_SPACE(256));
	nlh->nlmsg_len = NLMSG_SPACE(256);
	nlh->nlmsg_pid = getpid();
	nlh->nlmsg_flags |= NLM_F_REQUEST;
	nlh->nlmsg_type = NLMSG_MIN_TYPE + 1;

	strcpy(NLMSG_DATA(nlh), "Hello");

	iov.iov_base = (void *)nlh;
	iov.iov_len = nlh->nlmsg_len;

	memset(&msg, 0, sizeof(msg));
	msg.msg_name = (void *)&dest_addr;
	msg.msg_namelen = sizeof(dest_addr);
	msg.msg_iov = &iov;
	msg.msg_iovlen = 1;

	if (sendmsg(sock_fd, &msg, 0) < 0) {
		printf("%s\n", strerror(errno));
		return 2;
	}

	return 0;
}

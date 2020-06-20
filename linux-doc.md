# Linux Tools

## deb packages

You can install a `.deb` package by using:

```shell
sudo dpkg -i <deb_file>
sudo apt install -f
```

Another alternative is `gdeb` which will install all the dependencies automatically along with the package:

```shell
sudo gdebi <deb_file>
```

## dd

### Format disk

To format disk, use:

```shell
dd if=/dev/zero/ of=/dev/sd<?> conv=fdatasync status=progress
```

### Install ISO

To install ISO image on a disk:

```shell
dd bs=4M if=<path_to_ISO> of=/dev/sd<?> conv=fdatasync status=progress
```

Note: The `bs` option specifies size of one write, while `conv`, as set to `fdatasync` will ensure that all data is flushed to disk when `dd` is finished writing.

## Keyboard layout

To list available keyboard layouts, try finding `keymaps` folder somewhere in `/usr/share/`.

### Default

In the `keymaps` folder there is usually `defkeymap.kmap.gz` file. It can be reset to with `loadkeys -d`.

### Get current

To get current keyboard layout, use `dumpkeys`. On XServer, you can also see the layout with:

```shell
grep XKBLAYOUT /etc/default/keyboard
```

### Change layout

To change keyboard layout, you can use:

```shell
lodakeys <layout>
```

This won't work on XServer, however. In this case, use:

```shell
setxkbmap <layout>
```

## Shell variables

| var. |                 meaning                 |
|------|-----------------------------------------|
| `$?` | return value of latest executed command |
| `$!` | pid of latest executed command          |
| `$*` | arguments (to pass to another script)   |
| `$@` | arguments (to iterate over)             |
| `$#` | number of arguments                     |

## System info

Find out if system is 32bit or 64bit:

```shell
$ getconf LONG_BIT
64
```

To get architecture, simply use:

```shell
$ arch
armv7l
```

For general system info, use `uname -a`.

### System and service manager

To check whether `systemd` or `System V` is used, type:

```shell
[[ -e /run/systemd/system ]] && echo "systemd" || echo "System V"
```

## xargs

It is possible to pass `argument` as argument to command `command` using `xargs`:

```shell
argument | xargs -I {} command {}
```

The `{}` is a placeholder for the pipe input.

Note: To do a command for each line of input, you need to specify this with `-L` switch. Take a look at this example:

```shell
$ pgrep ksoft | xargs ps -o comm,cls,pri,pcpu,psr
COMMAND         CLS PRI %CPU PSR
ksoftirqd/0      TS  19  0.0   0
ksoftirqd/1      TS  19  0.0   1
ksoftirqd/2      TS  19  0.0   2
ksoftirqd/3      TS  19  0.0   3
$ pgrep ksoft | xargs -L 1 ps -o comm,cls,pri,pcpu,psr
COMMAND         CLS PRI %CPU PSR
ksoftirqd/0      TS  19  0.0   0
COMMAND         CLS PRI %CPU PSR
ksoftirqd/1      TS  19  0.0   1
COMMAND         CLS PRI %CPU PSR
ksoftirqd/2      TS  19  0.0   2
COMMAND         CLS PRI %CPU PSR
ksoftirqd/3      TS  19  0.0   3
```

## Error codes

Linux error codes can be found in `errno-base.h` and `errno.h` located in `/usr/include/asm-generic/` folder.

## Jobs

To see all jobs, type `jobs`. To put a job to foreground, use `fg <job_num>`. Similarly, to put a job to background, type `bg <job_num>`. You can put the current process to background with `CTRL + z` combination.

## xxd

### Standard hexdump

```shell
$ xxd <<< hello
00000000: 6865 6c6c 6f0a                           hello.
```

Note: You can also specify filename instead: `xxd <filename>`

### Raw hex output

```shell
$ xxd -ps <<< hello
68656c6c6f0a
```

### Hexdump to ASCII

```shell
$ xxd <<< hello | xxd -r
hello
```

Note: This is, sort of, equivalent to `echo hello | xxd | xxd -r`.

## column

You can arrange text in columns very easy with the `column` tool. Try this for example:

```shell
column -t -s':' /etc/passwd
```

## echo

|  switch   |           meaning           |
|-----------|-----------------------------|
|   `-n`    | don't add newline           |
|   `-e`    | interpret escape characters |

Note: From my experience this is depends on the shell (e.g. works on `bash`, but not `sh`).

Sometimes you will have to do an echo as a superuser. It is best accomplished by:

```shell
sudo sh -c 'echo "<text>" > <filename>'
```

## ls

### Sort by date

To sort by last modified date in ascending order:

```shell
ls -tr
```

### Get inode number

To get inode number of a file:

```shell
ls -i <file_name> | sed -n 's/^\([0-9]\+\)\s.*$/\1/p'
```

## grep

|  switch   |       meaning       |
|-----------|---------------------|
|   `-R`    | recursive           |
| `--color` | add color           |
|   `-n`    | print line          |
|   `-v`    | reverse             |
|   `-i`    | ignore case         |
|   `-B`    | show lines before   |
|   `-A`    | show lines after    |
|   `-q`    | quiet               |
|   `-c`    | count matched lines |

To find lines beggining with `STR`, type:

```shell
grep '^STR' <filename>
```

To find lines ending with `STR`, use:

```shell
grep 'STR$' <filename>
```

### grep AND

Without resorting to regex, just pipe grep into another:

```shell
grep 'STR1' | grep 'STR2'
```

### grep OR

You can use:

```shell
grep 'STR1\|STR2'
```

## awk

General syntax would be:

```shell
awk 'BEGIN { <code_on_begin> }; { <code_per_line> }; END { <code_on_end> }' <filename>
```

### Variables

| variable |      meaning     |
|----------|------------------|
|   FS     | input separator  |
|   OFS    | output separator |
|   NF     | number of fields |
|   NR     | line number      |

Note, you can pass variables from shell by using the `-v` switch:

```shell
TEST_VAR=Hello
echo "world" | awk -v test=$TEST_VAR '{ print test " " $0 }'
```

### Functions

You can define a function alongside the three main blocks:

```shell
awk 'BEGIN { ... }; function test(var){ ... }; { ... }; END { ... };' <filename>
```

### Regex

You can test if a variable conforms to a regex by using:

```awk
if(var ~ /<regex>/) { ... }
```

### Whitespace

You can use awk to trim leading and trailing whitespace:

```shell
$ echo "  test " | awk '{$1=$1;print}'
test
```

### Numeric operations

Standard arithmetic is supported in awk. One of the differences from `C` is the bitshift operation:

```shell
$ echo 3 | awk '{ print lshift(1,$1) }'
8
```

### Example 1

Print entries in `/etc/passwd` with line numbers and total line count:

```shell
$ awk 'BEGIN { FS=":"; lines=0 }; { print NR,$1; lines++ }; END { print "Total number of entries: " lines; }' /etc/passwd
```

### Example 2

List non-hidden folders with users (formatted as `<user> <- <folder>`):

```
$ ls -lahp | gawk 'BEGIN { OFS=" <- " }; { if($9 ~ /\/$/ && $9 !~ /^\./){ gsub("/$","",$9); print $3,$9 } }'
```

## syslog

```shell
logger <message>
```

To output syslog while waiting for new messages:

```shell
tail -f /var/log/syslog
```

## dmesg

To make `dmesg` wait and output new messages:

```shell
dmesg -w
```

## seq

To get a sequence of numbers from `a` to `b` with step `k`:

```shell
seq <a> <k> <b>
```

For example, to get every third number from 5 to 12, do:

```shell
$ seq 5 3 12
5
8
11
```

## sed

The lines passing through `sed` will be output by default. Try:

```shell
$ seq 1 2 7 | sed ''
1
3
5
7
```

Sometimes, you will want to control this behaviour with `-n` switch:

```shell
$ seq 1 2 7 | sed -n ''
```

In this case there is no output.

### Printing lines

To print the third line from the last example, type:

```shell
$ seq 1 2 7 | sed -n '3p'
5
```

To print every third line beginning with the fifth:

```shell
$ seq 1 1 17 | sed -n '5~3p'
5
8
11
14
17
```

### Removing lines

To remove a line, use the `d` command, e.g. remove the third line from the first five natural numbers:

```shell
$ seq 1 1 5 | sed '3d'
1
2
4
5
```

To remove every second line after (and including) the fourth line, try:

```shell
$ seq 1 1 10 | sed '4~2d'
1
2
3
5
7
9
```

To remove the last line:

```shell
$ seq 1 1 5 | sed '$d'
1
2
3
4
```

You can also negate the command with `!` sign:

```shell
$ seq 1 1 5 | sed '$!d'
5
```

### Replacing strings

To replace `STR1` with `STR2`, do:

```shell
sed 's/STR1/STR2/g' <filename>
```

Note: You can also use any other symbol instead of `/` as a delimiter:

```shell
sed 's_STR1_STR2_g' <filename>
```

Note: You can remove `g` at the end if you don't want it done across the whole input, but only on first match. To do operations in-place on the file, just add the `-i` switch.

Note: You can also pipe to `sed` instead of operating on a file:

```shell
$ echo "Hello world!" | sed 's/Hello/Bye/g'
Bye world!
```

### Prepend and append

To add `<char>` at the beginning of each line, type:

```shell
sed 's/^/<char>/' <filename>
```

Similarly, to append, use:

```shell
sed 's/$/<char>/' <filename>
```

Note: You can also do substitutions, prepends and appends on specific lines. Try:

```shell
$ seq 1 2 20 | sed '1~3s/$/#/' | sed '1~2s/^/#/' | sed '5s/#/-/'
#1#
3
#5
7#
-9
11
#13#
15
#17
19#
```

### Number of lines

To get the number of lines, you can, for example, do:

```shell
$ seq 1 1 5 | sed -n '$='
5
```

### Regex

It is possible to do regex with `sed`. Try:

```shell
$ seq 1 1 5 | sed 's/[23]/-&/'
1
-2
-3
4
5
```

The `&` represents the matched string.

### Newlines

Assume we have a shell with a lot of commands like:

```shell
echo -ne "(!) Could not open file.\n"
exit 4
```

We want to replace them with a function like the following:

```shell
error_and_exit "Could not open file." 4
```

We could do this by using:

```shell
sed -E ':begin;$!N;s/echo -ne "\(\!\) (.*)\\n"\nexit ([0-9]+)/error_and_exit "\1" \2/g;tbegin;P;D' <filename>
```

The `N` in the command will read another line of input and append it to the current line separated by newline (i.e. `\n`). This, however, means that the `sed` will only process every second line. To make it process each line, we add `P` (print) and `D` (delete) at the end. The `-E` switch is for extended regex.

### Example

Assume we have a list of songs:

```
01 - song1.mp3
02- song2.mp3
```

The whitespaces can be present, but not necessarily. We want to extract track number, song name and format. We could do this with:

```shell
sed -n 's/^\([0-9]\+\)\s*\?-\s*\?\(\w\+\)\.\(\w\+\)$/track: \1, name: \2, format: \3/p'
```

Note: In regular `sed`, it is not possible to do grouping without capturing (as is possible with some other regex conventions by using `(?:<pattern>)` syntax.

### Vim specific

To input whole file to `sed`, use `:%` as usual. To input a range, use, for example, `:2,$`. This will input a range from second line to the last one.

#### Number of lines

To get number of lines matching `STR1` in Vim, do:

```
:s/STR1//n
```

Also, if you want all matches (not just number of lines), use `gn` instead of `n` at the end.

## find

### Find executable

This will find all executable files (excluding searchable folders with `-type f` switch) in the specified folder:

```shell
find <folder> [OPTIONS] -executable -type f
```

### Quit on first match

To stop find on first match (and print it):

```shell
find <folder> [OPTIONS] -print -quit
```

### Execute on match

To execute command `<comm>` for each match, use:

```shell
find <folder> [OPTIONS] -exec <comm> {} \;
```

For example, to output contents of every shell script file:

```shell
find . -type f -executable -name "*.sh" -exec cat {} \;
```

Note: This is not really optimal as it creates subprocess for each match.

### Find links

To find links pointing to a specific file:

```shell
find -L / -samefile <filename>
```

To find links pointing to any file with specified filename:

```shell
find / -lname <filename>
```

## Audio

### PulseAudio

You can check if PulseAudio is up and running with:

```shell
$ pulseaudio --check
$ echo $?
0
```

#### Settings

PulseAudio settings are located in file `/etc/pulse/default.pa`.

#### Restart

To restart the daemon, you can just kill it and it will start again automatically:

```shell
pulseaudio -k
```

Note: You can also restart ALSA if problems persist:

```shell
pulseaudio -k && sudo alsa force-reload
```

Note: Sometimes it may also be necessary to start the PulseAudio daemon manually with:

```shell
pulseaudio -D
```

#### Fix crackling audio

If crackling or clicking is present when playing audio, usually it is resolved with either adding `tsched=0` or removing it from the following line in PulseAudio settings:

```shell
load-module module-udev-detect
```

Note: According to documentation, `tsched` is by default enabled, and that means PulseAudio will use a system-timer based module. If disabled (if hardware does not return accurate timing information), interrupt-based timing will be used instead.

Note: You can check if `tsched` is enabled with:

```shell
pacmd list | grep tsched
```

#### PulseAudio and JACK

You can use PulseAudio as a client to JACK server. First run:

```shell
apt install pulseaudio-module-jack
```

Note that this is distribution-dependant.

After that, run:

```shell
pacmd load-module module-jack-sink
pacmd load-module module-jack-source
```

You can also add these lines (without `pacmd`) in PulseAudio settings file.

Note: Alternative to `pacmd` is `pactl`, but former is preferred.

After running JACK, be sure to run:

```shell
pacmd set-default-sink jack_out
```

Note: This line can be put into "Execute script after Startup" in "Options" tab in `qjackctl` setup.

#### Sink operations

You can perform operations on sinks, such as set volume, mute, etc. To get a list of sinks, use:

```shell
pacmd list-sinks | grep index -nA2
```

Similarly, you can see current volume settings for specific sinks:

```shell
pacmd list-sinks | grep 'index\|^\s\+volume:'
```

Then, to, for example, set volume for a specific sink, run:

```shell
pacmd set-sink-volume <sink_index> <sink_volume>
```

#### PulseAudio GUI control

If necessary, you can use `pavucontrol` to control PulseAudio.

### JACK

To start `jackd` use:

```shell
jackd -d <driver>
```

You can use `-h` to get help for specific driver:

```shell
jackd -d <driver> -h
```

Note: For ALSA, use:

```shell
jackd -d alsa
```

#### Connections

To see a list of JACK clients:

```shell
jack_lsp
```

You can then connect clients with:

```shell
jack_connect <client_1> <client_2>
```

Note: To disconnect, just use `jack_disconnect` in the same manner as above.

#### JACK over network

On master (where audio will be output to speakers), after running JACK, also run:

```shell
jack_load netmanager
```

This will setup JACK network server.

On slave (from where audio will be played), simply run `jackd` with:

```shell
jackd -d net -a <server_ip>
```

For additional options, see:

```shell
jackd -d net -h
```

Note: This step for slave may not be necessary; usually it is enough to set up `net` as driver in `qjackctl` and start the JACK server.

## Networking

### GUI via SSH

You can run GUI applications on host with:

```shell
ssh -Y <username>@<address>
```

Note: If the `-Y` switch does not work, use `-X` (less secure). You can also use `-XY` to try both.

Note: Once connected, you can run the GUI application on remote display by typing:

```shell
export DISPLAY=:0
```

Note: You can also forward mouse and keyboard by installing `x2x` on host and then running:

```shell
ssh -X <username>@<address> 'x2x -east -to :0'
```

### ip

The source code for various ip utils like `ip link` and `ip netns` can be found [here](https://github.com/shemminger/iproute2/tree/master/ip). A good tutorial for various virtual network models (via `ip link`) is located [here](https://developers.redhat.com/blog/2018/10/22/introduction-to-linux-interfaces-for-virtual-networking/#bridge).

#### List links

You can get the list of all links (across all namespaces) by using:

```shell
ip link list
```

This is similar to `ifconfig -a`.

#### List network namespaces

To list all network namespaces:

```shell
ip netns list
```

The command `ip netns show` is the same.

#### Add netns

You can add a network namespace via:

```shell
ip netns add <netns_name>
```

#### Execute within netns

You can run any shell command within the specified network namespace by using:

```shell
ip netns exec <netns_name> <command>
```

For example, you can easily use `ifconfig` as a command. Similar result can be obtained by:

```shell
ip netns exec <netns_name> ip link list
```

This will give you a list of links within the specified network namespace.

#### Move link to a namespace

To move a link to a specific namespace, use:

```shell
ip netns exec <old_netns> ip link set <link_name> netns <new_netns>
```

### Scan network for devices

First, find the IP range for the desired interface (e.g. `eth0`):

```shell
ip addr show <interface> | sed -n 's/^ \+inet \([0-9\.\/]\+\).*$/\1/p'
```

This one will print out IP with subnet mask in CIDR format, which you can use directly in nmap:

```shell
nmap -sn <ip_with_CIDR>
```

Note: You can get the IP and subnet mask by using:

```shell
ifconfig <interface> | grep 'inet\s' | awk '{ print $2 OFS $4 }'
```

The only thing to note here is that you have to convert the subnet mask to CIDR, and you can do that with:

```shell
echo <subnet_mask> | python3 -c 'import sys; print(len([x for x in "".join(list(map(lambda o: bin(int(o,10))[2:].zfill(8), sys.stdin.read().split(".")))) if x == "1"]))' | xargs -I {} echo "/{}"
```

### NFS

When sharing files between Linux machines, it is best to use NFS. To set up a shared folder on the server, first be sure to install `nfs-kernel-server` and `nfs-common` (Ubuntu/Debian) or `nfs-utils` (Arch).

Once installed, edit `/etc/exports` to add something like:

```shell
/path/to/shared/fs	192.168.5.1/24(rw,no_root_squash,async)
```

You already have a few examples in the forementioned file.

Restart the `nfs-kernel-server` with:

```shell
service nfs-kernel-server restart
```

Note, the same can be accomplished with:

```shell
sudo /etc/init.d/nfs-kernel-server restart
```

You can verify that everything is set up properly by typing:

```shell
showmount -e
```

Finally, on the client-side (after installing `nfs-common`):

```shell
mount -t nfs <ip_addr>:/path/to/shared/fs /path/to/mount
```

## ldconfig

### List

To see a list of installed libraries use:

```shell
ldconfig -p | grep <lib_name>
```

### Update

To update after installing or removing libraries, just run:

```shell
ldconfig
```

Note: You may need to run this as root.

## Devices

To get a list of all devices, use:

```shell
lshw
```

The link to source code is [here](https://github.com/lyonel/lshw), along with list of search paths.

### Block devices

List block devices:

```shell
lsblk
```

Basically the information is derived from `/sys/block/` folder (and its subfolders).

### PCI devices

List PCI devices:

```shell
lspci
```

The information is obtained by parsing:

```
/sys/bus/pci/devices/<device>/config
```

This is not human-readable, however. Usually there is a file called `pci.ids` on the system, possibly somewhere in `/usr/share/` folder.

### USB devices

List USB devices (use `-v` switch for more information on each device):

```shell
lsusb
```

There is also an alternative:

```shell
usb-devices
```

You can find all this information manually in the `/sys/bus/usb/devices` folder. To find the driver:

```shell
readlink /sys/bus/usb/devices/<device>/driver
```

To find which specific kernel module is responsible:

```shell
/sbin/modinfo /sys/bus/usb/devices/<device>/modalias
```

### Network devices

To find the driver of a physical network device (e.g. `eth0`), use:

```shell
readlink /sys/class/net/<device>/device/driver
```

Note: For a virtual network device (e.g. `lo`), there is no link pointing to the driver, but, you can find information about it in `/sys/devices/virtual/net/<device>` folder.

### Displays

It's best to get info on displays using `xrandr`.

#### Primary display size

Here is a one-liner using `xrandr` to get display size (diagonal) in inches:

```shell
xrandr | grep primary | sed -n 's/^.*\s\([0-9]\+\)mm\sx\s\([0-9]\+\)mm$/\1x\2/p' | python3 -c 'import sys; dim = tuple(map(lambda s: (int(s, 10) / 25.4 )**2, sys.stdin.read()[:-1].split("x"))); print((dim[0] + dim[1])**0.5)'
```

## Filesystem

### Create a file

A bit advanced tool to create a file is:

```shell
mknod <pathname> <mode> <major> <minor>
```

For `<mode>` you can choose:

|   mode   |               meaning               |
|----------|-------------------------------------|
|   `b`    | block (buffered) special file       |
| `c`, `u` | character (unbuffered) special file |
|   `p`    | FIFO                                |

### Temporary files

To create a temporary file with a unique name:

```shell
$ mktemp
/tmp/tmp.teJqtZlPqv
```

Permissions are set to `600`. If provided with template, it will create it in the current folder:

```shell
$ mktemp test.XXX
test.jEQ
```

Note: The duration of the file is system and location dependant.

#### `tmpfs` and `ramfs`

To create a temporary filesystem (all files created there reside only in RAM), use, e.g.:

```shell
mount -t tmpfs -o size=50m tmpfs <mount_point>
```

This will create a `tmpfs` partition of 50 megabytes.

Note: You can view all mounted filesystems (in pretty-print) by using `df -h`.

Note: Similarly, you can use `ramfs`; the only difference is the `ramfs` will grow dynamically as space is used, and the system might crash when all RAM is consumed. On the other hand, `tmpfs` will not grow dynamically (it is fixed on the specified size), and might use swap space if out of RAM.

# Git

## List tracked files

```shell
git ls-tree -r master --name-only
```

## List incoming / outgoing commits

After doing a `git fetch`, you might want to see commits that have been loaded from upstream:

```shell
git log ..origin/master
```

This is more useful than doing a `git pull`, as you might want to check commits, cherry pick them or rebase. Similarly, for outgoing commits:

```shell
git log origin/master..
```

If you are satisfied, you can simply use:

```shell
git rebase origin/master
```

This is usually better than `git pull` which will create a merge commit in between.

## Make local branch equal to remote

You can do this simply with:

```shell
git reset --hard origin/master
```

Note: This, just as examples above, assume that remote you are operating on is `origin` and the branch is `master`.

## Rebase onto

To rebase all commits from commit `A` on top of commit `B`, use:

```shell
git rebase --onto <new_parent> <old_parent>
```

Here, `new_parent` is commit `B` and `old_parent` is commit `A`.

## Various lists

To see all branches, do:

```shell
git branch -a
```

To see all remotes, do:

```shell
git remote -v
```

## Unstage file

To unstage a file:

```shell
git reset -- <filename>
```

## tmux

|        action       |    shortcut   |
|---------------------|---------------|
| TCRL                |  `CTRL + b`   |
| Split window (hor.) |  `TCRL & "`   |
| Split window (ver.) |  `TCRL & %`   |
| Window full screen  |  `TCRL & z`   |

## Vim

### Shortcuts

|        action       |    shortcut   |
|---------------------|---------------|
| WCRL                |  `CTRL + w`   |
| Home                |      `^`      |
| End                 |      `$`      |
| Beginning of doc.   |      `gg`     |
| End of document     |      `G`      |
| Top of screen       |      `H`      |
| Bottom of screen    |      `L`      |
| New window (ver.)   |  `WCRL & v`   |
| New window (hor.)   |  `WCRL & s`   |
| Next word (beg.)    |      `w`      |
| Prev word (beg.)    |      `b`      |
| Next word (end)     |      `e`      |
| Prev word (end)     |      `ge`     |
| Insert before       |      `i`      |
| Insert at line beg. |      `I`      |
| Insert after        |      `a`      |
| Insert at line end  |      `A`      |
| Page forward (down) |   `CTRL + f`  |
| Page back (up)      |   `CTRL + b`  |
| Selection           |      `v`      |
| Visual block        |   `CTRL + v`  |
| Undo                |      `u`      |
| Redo                |   `CTRL + r`  |
| Replace (once)      |      `r`      |
| Replace (mode)      |      `R`      |
| Copy (yank)         |      `y`      |
| Cut                 |      `dd`     |
| Paste after         |      `p`      |
| Paste before        |      `P`      |
| Indent              |      `>`      |
| Unindent            |      `<`      |

Note: The `&` means here "followed by" and not "at the same time" (which is `+`).

### Commands

|    command    |     action      |
|---------------|-----------------|
| `:e <fname>`  | open file       |
|     `:w`      | save changes    |
|     `:q`      | quit            |
|`:colorscheme` | set colorscheme |

### Miscellaneous

|  symbol  |              meaning             |
|----------|----------------------------------|
|   `%`    |  input whole file                |
|   `$`    |  input last line                 |
| `<num>`  |  input line `<num>`              |
|`:<a>,<b>`|  input range from `<a>` to `<b>` |

### Search

See:

```
:help /\c
:help /\C
:help 'smartcase'
```

### Shell

To pipe input to a shell command, you can use the selection or visual block, and write something like this:

```
:'<,'>w !grep "hello" --color
```

This is particularly useful if using `xclip`:

```
:'<,'>w !xclip -selection clipboard
```

To read output from a shell command, and insert it as text, use:

```
:r !ls
```

Similarly, for `xclip`:

```
:r !xclip -o -selection clipboard
```

## GDB basics

To insert a breakpoint by line number:

```
(gdb) break <source_file>:<line_number>
```

Also, you can break at a particular function:

```
(gdb) break <source_file>:<function_name>
```

Then, you can simply use:

```
(gdb) run
```

To do a step after running stops (after a breakpoint):

```
(gdb) step
```

Similarly, to do a step, but without entering a function call, use:

```
(gdb) next
```

To see values of current variables:

```
(gdb) info locals
```

To step back out of function invocation:

```
(gdb) finish
```

To continue execution until next breakpoint:

```
(gdb) continue
```

# ARM Assembly

## commands

### add

```
ADD Rd, Rm, Rn <=> Rd = Rm + Rn
```

`Rn` is flexible.

### multiply

```
MUL Rd, Rm, Rn <=> Rd = Rm * Rn
```

`Rn` is not flexible.

### bit clear

```
BIC Rd, Rs <=> Rd = Rd & !Rs
```

This is a "reverse mask". That is, where `Rs` is `1`, it will set the bits in `Rd` to `0`.


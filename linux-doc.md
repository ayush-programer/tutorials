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
| `$$` | current process pid                     |

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

To check whether systemd or System V is used, type:

```shell
[[ -e /run/systemd/system ]] && echo "systemd" || echo "System V"
```

#### systemd

##### Start program on boot

Create a file with `.service` suffix in `/etc/systemd/system/` folder. It should minimally contain:

```
[Unit]
After=<service_or_target_name>

[Service]
ExecStart=<command_or_script>

[Install]
WantedBy=<service_or_target_name>
```

You can find list of services and targets by using:

```shell
ls /lib/systemd/system/{*.target,*.service} | xargs -L1 basename
```

Field explanations:

 * `After` - instructs systemd on when the script should be run
 * `ExecStart` - command or script to execute
 * `WantedBy` - into what boot target the unit should be installed

Additional common fields:

 * `Description` - describes the unit
 * `Type` - two common types are `simple` and `oneshot` (useful if the command issued by `ExecStart` exists); see man pages for other types
 * `RemainAfterExit` - useful if the type is `oneshot` as even when the command exits, systemd will consider the service active
 * `Environment` - provide environment variables

Note: You can find all necessary information by using:

```shell
man systemd.service
```

Make the `.service` file executable (for example, with `chmod 744`). It may be necessary to reload the services:

```shell
systemctl daemon-reload
```

Then, enable the unit with:

```shell
systemctl enable <service_name>
```

The unit will start after reboot. You can, however, do it manually with:

```shell
systemctl start <service_name>
```

Note: The corresponding commands for the former and latter are `disable` and `stop`, respectively.

## xargs

It is possible to pass `argument` as argument to command `command` using `xargs`:

```shell
argument | xargs -I {} command {}
```

The `{}` is a placeholder for the pipe input.

Note: To do a command for each line of input, you need to specify this with `-L` switch. Take a look at these examples:

```shell
$ pgrep ksoft | xargs ps -o comm,cls,pri,pcpu,psr
COMMAND         CLS PRI %CPU PSR
ksoftirqd/0      TS  19  0.0   0
ksoftirqd/1      TS  19  0.0   1
ksoftirqd/2      TS  19  0.0   2
ksoftirqd/3      TS  19  0.0   3
```

```shell
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

## IPC

You can see processes using the IPC (Inter-Process Communication) with the `ipcs` command.

## watch

You can run a command periodically and highlight differences using:

```shell
watch -n <sec> -d <command>
```

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

## du

To get the size of a folder, use:

```shell
du -sh <folder>
```

## echo

|  switch   |           meaning           |
|-----------|-----------------------------|
|   `-n`    | don't add newline           |
|   `-e`    | interpret escape characters |

Note: From my experience this depends on the shell (e.g. works in `bash`, but not in `sh`).

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

### Range

To input a range, use, for example, `2,$` as prefix. This will input a range from second line to the last one.

```sh
$ seq 1 5 | sed -n '3,$p'
3
4
5
```

Note: Similarly, to print from first to third:

```sh
$ seq 1 5 | sed -n '1,3p'
1
2
3
```

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

## Shell Parameter Expansion

You can find out more about shell parameter expansion [here](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html).

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
#### Real-time privileges

First make sure that your user is part of `audio` group:

```shell
usermod -a -G audio <username>
```

Note: Group name for JACK might differ on some distributions, so, if there is no `audio` group check for 'jackuser' or similar names before adding the group yourself with `groupadd audio`.

Then, add the following lines to `/etc/security/limits.d/audio.conf` (create it if it does not exist):

```
@audio	-	rtprio	95
@audio	-	memlock	unlimited
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

#### Autostart JACK

JACK can be autostarted via systemd service. Note that this is not the preferred way of doing, as JACK was not designed as a system-wide replacement for PulseAudio, and requires XServer. However, a few hacks can enable JACK to be started without XServer via systemd; just copy the following contents to `/etc/systemd/system/jackd.service`:

```
[Unit]
Description=JACK daemon
After=sound.target

[Service]
LimitRTPRIO=infinity
LimitMEMLOCK=infinity
Environment='JACK_NO_AUDIO_RESERVATION=1'
User=<user_name>
ExecStart=/usr/bin/jackd -R -d alsa

[Install]
WantedBy=multi-user.target
```

Then, simply enable the service with `systemctl enable jackd.service`.

### OpenAL

OpenAL can be configured by editing the following file:

```
/etc/openal/alsoft.conf
```

Note: If there are issues with `alsoft` JACK client, you can always force OpenAL to use PulseAudio and then connect PulseAudio with JACK (as described above). In this case, make sure that driver is properly configured in `alsoft.conf`:

```
driver = pulse
```

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

You already have a few examples in the forementioned file. Also, you can read about all options with:

```shell
man exports
```

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

#### Filesystem info

To get information on filesystems per partition, use:

```shell
file -sL /dev/sd*
```

Note: You can also use `blkid`.

#### Format disk

To format disk, use:

```shell
dd if=/dev/zero/ of=/dev/sd<?> conv=fdatasync status=progress
```

#### Install ISO

To install ISO image on a disk:

```shell
dd bs=4M if=<path_to_ISO> of=/dev/sd<?> conv=fdatasync status=progress
```

Note: The `bs` option specifies size of one write, while `conv`, as set to `fdatasync` will ensure that all data is flushed to disk when `dd` is finished writing.

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


## Terminal multiplexing

### GNU Screen

#### Shortcuts

|        action       |    shortcut   |
|---------------------|---------------|
| SCRL                |  `CTRL + a`   |
| Open console        |  `SCRL + :`   |
| Detach              |  `SCRL + d`   |
| Split screen        |  `SCRL & |`   |
| Next screen         | `SCRL & TAB`  |
| Close screen        |  `SCRL & X`   |
| Create window       |  `SCRL & C`   |
| Next window         |  `SCRL & n`   |
| Previous window     |  `SCRL & p`   |
| Kill window         |  `SCRL & k`   |
| Copy mode           |  `SCRL & [`   |
| Paste buffer        |  `SCRL & ]`   |
| Log current screen  |  `SCRL & h`   |
| Start/end logging   |  `SCRL & H`   |
| Lock screen         |  `SCRL & x`   |
| Help                |  `SCRL & ?`   |

Note: Next and previous window will change windows inside current screen. Also, close screen will not close the window it is displaying.

Note: In copy mode, navigate as in Vim. To copy text, trigger select with space or return key.

#### Create session

You can create session by simply calling `screen`. You can create a named screen session by using:

```sh
screen -S <name>
```

#### List sessions

To list current screen sessions:

```sh
screen -list
```

#### Reattach to a session

To reattach to a session, try:

```sh
screen -r <pid>
```

Note: You don't have to specify PID, using only `screen -r` will attach you to the last used screen session.

### `tmux`

|        action       |    shortcut   |
|---------------------|---------------|
| TCRL                |  `CTRL + b`   |
| Split window (hor.) |  `TCRL & "`   |
| Split window (ver.) |  `TCRL & %`   |
| Window full screen  |  `TCRL & z`   |

## Vim

### Generic shortcuts

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
| Next occurrence     |      `*`      |
| Previous occurrence |      `#`      |
| Repeat last search  |      `n`      |
| Prev. last search   |      `N`      |
| Show current file   |`1 & CTRL + g` |
| Curr. file and buff.|`2 & CTRL + g` |

Note: The `&` means here "followed by" and not "at the same time" (which is `+`).

### Commands

|      command      |              action            |
|-------------------|--------------------------------|
|   `:e <fname>`    | open file                      |
|      `:pwd`       | get current folder             |
|    `:cd <dir>`    | change directory               |
|    `:lcd <dir>`   | change dir. for current window |
|       `:w`        | save changes                   |
|       `:q`        | quit                           |
|  `:colorscheme`   | set colorscheme                |
| `:Explore <path>` | explore in `netrw`             |

### Buffers

|      command      |     action         |
|-------------------|--------------------|
| `:ls`, `:buffers` | list buffers       |
|  `:buffer <num>`  | open buffer        |
|     `:bnext`      | next buffer        |
|     `:bprev`      | previous buffer    |
|   `:bdel <num>`   | delete buffer      |

Note: You can delete all buffers and edit the last with `:%bd|e#`.

### Edit via SSH

You can edit files via SSH with:

```sh
vim scp://<user>@<host>/path/to/file
```

Similarly, you can use the same as in-editor command:

```
:e scp://<user>@<host>/path/to/file
```

### Input ranges

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

### `ctags`

|        action       |    shortcut   |
|---------------------|---------------|
| Go to selected tag  |  `WCRL + ]`   |
| Back to prev. tag   |  `WCRL + t`   |

Note: You can also use the following commands:

|       command       |    shortcut   |
|---------------------|---------------|
| Search for a tag    |  `:ts <tag>`  |
| Next definition     |    `:tn`      |
| Previous definition |    `:tp`      |

#### Generate tags file

To generate tags file for a folder (and its subfolders), use:

```shell
ctags -R
```

Similarly, you can generate tags for the Linux kernel source with:

```shell
make tags
```

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

## Apply patch to single file

You can use `include` argument to filter the files to which the patch will be applied:

```shell
git apply --include=<path-pattern> <patch-file>
```

# GDB basics

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

# U-Boot

## Example compile for RPi 3B+

First, clone U-Boot repo:

```shell
git clone --depth 1 --branch v2017.11 git://git.denx.de/u-boot.git v2017.11
```

Then, to compile for 64-bit:

```shell
sudo make -C v2017.11/ CROSS_COMPILE=aarch64-linux-gnu- rpi_3_defconfig
sudo make -C v2017.11/ CROSS_COMPILE=aarch64-linux-gnu-
```

This will create a `u-boot.bin` file which you can find in one of repo subfolders.

Note: If using Ubuntu, you can install `aarch64` toolchain with:

```shell
sudo apt install gcc-aarch64-linux-gnu
```

Then, create file `config.txt` that will be copied onto RPi SD card, along with `u-boot.bin`:

```shell
// config.txt

# Serial console output!
enable_uart=1

# 64bit-mode
arm_control=0x200

# Use U-Boot
kernel=u-boot.bin

device_tree_address=0x100
device_tree_end=0x8000

dtparam=i2c_arm=on
dtparam=spi=on
```

### Booting Raspbian

Create `rpi3-bootscript.txt`:

```shell
// rpi3-bootscript.txt

setenv kernel_addr_r 0x01000000
setenv ramdisk_addr_r 0x02100000
fatload mmc 0:1 ${kernel_addr_r} boot/Image
fatload mmc 0:1 ${ramdisk_addr_r} boot/initrd.img
setenv initrdsize $filesize
booti ${kernel_addr_r} ${ramdisk_addr_r}:${initrdsize} ${fdt_addr_r}
```

You can compile it with:

```shell
mkimage -T script -n 'Bootscript' -C none -d ~/<input_file> ~/<output_file>.scr
```

In this case, for example:

```shell
sudo mkimage -A arm64 -O linux -T script -d ~/rpi3-bootscript.txt ~/boot.scr
```

Note: In general, you should be able to use `source` from U-Boot to load the script.

Note: If you don't have `initrd.img`, you can omit loading it to memory and then use `booti $kernel_addr_r - $fdt_addr_r` instead.

### Running custom Yocto RPi image

Before building the project, to use the serial console, add the following in the `conf/local.conf` in your Poky build folder:

```
RPI_USE_U_BOOT = "1"
ENABLE_UART = "1"
```

After the build is complete, find the `Image` file from the Poky build folder and copy it to bootfs partition of the SD card:

```shell
find tmp/deploy/images/<rpi_image>/ -name Image
```

Then, find the rootfs file and extract it to rootfs partition of the SD card:

```shell
find tmp/deploy/images/<rpi_image>/ -name *.tar.bz2
tar -C <dest_dir> -xvjf <path_to_rootfs_bz>
```

Finally, find the Device Tree Blob / Binary in the build folder by typing:

```shell
find tmp/deploy/images/<rpi_image>/ -name *.dtb
```

Select the one for the board you need. After loading the kernel and the Device Tree Blob, either via `fatload` or `loady`, type the following in U-Boot:

```
setenv bootargs 8250.nr_uarts=1 console=ttyS0,115200 root=/dev/mmcblk0p2 rootfstype=ext4 rootwait
booti $kernel_addr_r - $fdt_addr_r
```

## Serial console

You can access U-Boot via serial console (serial to USB adapter needed, though): 

```shell
screen /dev/ttyUSB0 115200
```

Similarly, you can use `minicom`.

## Load file via serial console

If using Ubuntu, make sure to run:

```shell
sudo apt install lrzsz
```

You can easily load file to memory address by using:

```
U-Boot> loady <addr>
```

U-Boot will then wait for transfer.

### Minicom

While U-Boot is waiting for transfer, go to help (`CTRL+a & z`), as indicated in Minicom status bar below. Then, type `s` to send the file, and choose `ymodem`. Here you can select the file to upload via the serial console to U-Boot.

### GNU Screen

While U-Boot is waiting for transfer, go to Screen console and type:

```
exec !! sx path/to/file
```

Note: If using `socat`, you can transfer the file from shell, e.g.:

```shell
sx path/to/file | socat FILE:/dev/ttyUSB0,b115200,raw -
```

## Execute binary

You can execute a standalone program by using:

```shell
go <addr>
```

Note: For Linux kernel and similar programs which require line parameters, you should use `bootm`.

## Read from memory address

To read a byte from memory address, use:

```
md.b <address> <number_of_objects>
```

Note: All arguments are in hexadecimal.

Note: You can also use `md.w`, `md.l` and `md.q` to read 2, 4 and 8 bytes, respectively.

# ARM Architecture

The best place to find information on ARM (Advanced RISC Machine) Architecture is [here](https://developer.arm.com/documentation/).

## ARMv7

A32 is the instruction set named ARM in the ARMv7 architecture; A32 uses 32-bit fixed-length instructions.

## ARMv8

Aarch64 and Aarch32 are the 64-bit and 32-bit general-purpose register width states of the ARMv8 architecture. Aarch32 is broadly compatible with the ARMv7-A architecture.

### Registers

|   register   |             purpose              |
|--------------|----------------------------------|
|     `x0`     | parameter / temporary / result   |
|  `x1 - x7`   | parameter / temporary            |
|     `x8`     | indirect result location         |
|  `x9 - x15`  | scratch                          |
| `x16 - x17`  | intra-procedure-call / temporary |
|    `x18`     | platform register / temporary    |
| `x19 - x28`  | callee-saved / temporary         |
|    `x29`     | frame pointer                    |
|    `x30`     | link register                    |
|     `sp`     | stack pointer                    |
|    `xzr`     | zero register                    |

Note: Sometimes, "non-volatile" is used as synonym for "callee-saved".

Note: Frame pointer is useful for debugging; it should point at the top of the stack for the current function. The link register is the address to which the program counter will return to after current function exits.

Note: The corresponding 32-bit registers are prefixed by `w` (word) instead of `x` (extended word).

Note: More information on register and procedure conventions (AAPCS64) for AArch64 can be found [here](https://developer.arm.com/documentation/ihi0055/c/).

### A64

A64 is the instruction set available in AArch64 state.

#### Add

```
ADD Rd, Rm, Rn <=> Rd = Rm + Rn
```

`Rn` is flexible.

#### Multiply

```
MUL Rd, Rm, Rn <=> Rd = Rm * Rn
```

`Rn` is not flexible.

#### Bitwise `and`

```
and Rd, Rs <=> Rd = Rd & Rs
```

#### Bit Clear

```
bic Rd, Rs <=> Rd = Rd & !Rs
```

This is a "reverse mask". That is, where `Rs` is `1`, it will set the bits in `Rd` to `0`.

#### Bitwise OR

```
orr Rd, Rs <=> Rd = Rd | Rs
```

#### Bitwise XOR

```
eor Rd, Rs <=> Rd = Rd XOR Rs
```

#### Compare and Branch

Compare and Branch if Zero:

```
cbz Rs, label <=> if (Rs == 0) goto label
```

Compare and Branch if Not Zero:

```
cbnz Rs, label <=> if (Rs != 0) goto label
```

### System registers

You can find an extensive list of AArch64 System Registers [here](https://developer.arm.com/docs/ddi0595/h/aarch64-system-registers). Usually, each system register can be read by using:

```
mrs Rd, <register>
```

#### Multiprocessor Affinity Register

Used to identify CPU cores and clusters. Read with:

```
mrs Rd, mpidr_el1
```

For example, to find out the core on which the code is running:

```
mrs x0, mpidr_el1
and x0, x0, 0xFF
```

Register `x0` will contain core ID.

#### Current Exception Level Register

Use the following command to get the current exception level:

```
mrs Rd, CurrentEL
```

# x86 Architecture

You can find extensive documentation on x86 architecture [here](https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html).

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

## xargs

It is possible to pass `argument` as argument to command `command` using `xargs`:

```shell
argument | xargs -I{} command {}
```

The `{}` is a placeholder for the pipe input.

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

To sort by last modified date in ascending order:

```shell
ls -tr
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
sed -n 's/^\([0-9]\+\)s*-\s*\?\(\w\+\)\.\(\(\w\|[0-9]\)\+\)$/track: \1, name: \2, format: \3/p'
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

## ip

### List network namespaces

To list all network namespaces:

```shell
ip netns list
```

The command `ip netns show` is the same.

### List links

You can get the list of all links (across all namespaces) by using:

```shell
ip link list
```

This is similar to `ifconfig -a`.

### Add netns

You can add a network namespace via:

```shell
ip netns add <netns_name>
```

### Execute within netns

You can run any shell command within the specified network namespace by using:

```shell
ip netns exec <netns_name> <command>
```

For example, you can easily use `ifconfig` as a command. Similar result can be obtained by:

```shell
ip netns exec <netns_name> ip link list
```

This will give you a list of links within the specified network namespace.

### Move link to a namespace

To move a link to a specific namespace, use:

```shell
ip netns exec <old_netns> ip link set <link_name> netns <new_netns>
```

## nmap

## Number conversions

You can use Python to convert from hex to decimal, binary, etc., as it can easily be called from the shell:

```shell
python -c "<command>"
```

To convert from decimal to binary:

```python
>>> bin(43)
'0b101011'
```

To cut the '0b', use:

```python
>>> bin(43)[2:]
'101011'
```

To further format the output, you can use:

```python
>>> bin(43)[2:].zfill(8)
'00101011'
```

To convert a string to to an integer of base 16:

```python
>>> int('57', 16)
87
```

To convert a number to a string, use:

```python
>>> str(43)
'43'
```

## Filesystem

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

# Git

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

# tmux

|        action       |    shortcut   |
|---------------------|---------------|
| TCRL                |  `CTRL + b`   |
| Split window (hor.) |  `TCRL & "`   |
| Split window (ver.) |  `TCRL & %`   |
| Window full screen  |  `TCRL & z`   |

# Vim

## Shortcuts

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

## Commands

|    command    |     action      |
|---------------|-----------------|
| `:o <fname>`  | open file       |
|     `:w`      | save changes    |
|     `:q`      | quit            |
|`:colorscheme` | set colorscheme |

## Miscellaneous

|  symbol  |              meaning             |
|----------|----------------------------------|
|   `%`    |  input whole file                |
|   `$`    |  input last line                 |
| `<num>`  |  input line `<num>`              |
|`:<a>,<b>`|  input range from `<a>` to `<b>` |

## Search

See:

```
:help /\c
:help /\C
:help 'smartcase'
```

## Shell

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

# Makefile

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


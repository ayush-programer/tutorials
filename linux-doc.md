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

## shell variables

| var. |                 meaning                 |
|------|-----------------------------------------|
| `$?` | return value of latest executed command |
| `$!` | pid of latest executed command          |
| `$*` | arguments (to pass to another script)   |
| `$@` | arguments (to iterate over)             |
| `$#` | number of arguments                     |

## system info

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

## xxd

### standard hexdump

```shell
$ echo hello | xxd
00000000: 6865 6c6c 6f0a                           hello.
```

Note: You can also specify filename instead: `xxd <filename>`

### raw hex output

```shell
$ echo hello | xxd -ps
68656c6c6f0a
```

### hexdump to ASCII

```shell
$ echo hello | xxd | xxd -r
hello
```

## column

You can arrange text in columns very easy with the `column` tool. Try this for example:

```shell
cat /etc/passwd | column -t -s':'
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

|  switch   |      meaning      |
|-----------|-------------------|
|   `-R`    | recursive         |
| `--color` | add color         |
|   `-n`    | print line        |
|   `-v`    | reverse           |
|   `-i`    | ignore case       |
|   `-B`    | show lines before |
|   `-A`    | show lines after  |
|   `-q`    | quiet             |

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

## gawk

General syntax would be:

```shell
gawk 'BEGIN { <code_on_begin> }; { <code_per_line> }; END { <code_on_end> }'
```

### variables

| variable |      meaning     |
|----------|------------------|
|   FS     | input separator  |
|   OFS    | output separator |
|   NF     | number of fields |
|   NR     | line number      |

### example 1

Print entries in `/etc/passwd` with line numbers and total line count:

```shell
$ cat /etc/passwd | gawk 'BEGIN { FS=":"; lines=0 }; { print NR,$1; lines++ }; END { print "Total number of entries: " lines; }'
```

### example 2

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

### printing lines

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

### removing lines

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

### replacing strings

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

### prepend and append

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

### regex

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

### newlines

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

### Vim specific

To input whole file to `sed`, use `:%` as usual.

To get number of lines matching `STR1` in Vim, do:

```
:s/STR1//n
```

Also, if you want all matches (not just number of lines), use `gn` instead of `n` at the end.

## find

### find executable

This will find all executable files (excluding searchable folders with `-type f` switch) in the specified folder:

```
find <folder> [OPTIONS] -executable -type f
```

### quit on first match

To stop find on first match (and print it):

```
find <folder> [OPTIONS] -print -quit
```

## kernel modules

|   comm   |        meaning       |
|----------|----------------------|
| `lsmod`  | list kernel modules  |
| `insmod` | insert kernel module |
| `rmmod`  | remove kernel module |

## ip

### list network namespaces

To list all network namespaces:

```shell
ip netns list
```

The command `ip netns show` is the same.

### list links

You can get the list of all links (across all namespaces) by using:

```shell
ip link list
```

This is similar to `ifconfig -a`.

### add netns

You can add a network namespace via:

```shell
ip netns add <netns_name>
```

### exec within netns

You can run any shell command within the specified network namespace by using:

```shell
ip netns exec <netns_name> <command>
```

For example, you can easily use `ifconfig` as a command. Similar result can be obtained by:

```shell
ip netns exec <netns_name> ip link list
```

This will give you a list of links within the specified network namespace.

### move link to a namespace

To move a link to a specific namespace, use:

```shell
ip link set <link_name> netns <netns_name>
```

## nmap

## number conversions

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

## filesystem

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

## list incoming / outgoing commits

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

## rebase onto

To rebase all commits from commit `A` on top of commit `B`, use:

```shell
git rebase --onto <new_parent> <old_parent>
```

Here, `new_parent` is commit `B` and `old_parent` is commit `A`.

## various lists

To see all branches, do:

```shell
git branch -a
```

To see all remotes, do:

```shell
git remote -v
```

## tmux

|        action       |    shortcut   |
|---------------------|---------------|
| TCRL                |  `CTRL + b`   |
| Split window (hor.) |  `TCRL & "`   |
| Split window (ver.) |  `TCRL & %`   |
| Window full screen  |  `TCRL & z`   |

# Vim

## shortcuts

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

## commands

|    command    |     action      |
|---------------|-----------------|
| `:o <fname>`  |  open file      |
|     `:w`      |  save changes   |
|     `:q`      |  quit           |

## misc

|  symbol  |        meaning       |
|----------|----------------------|
|   `%`    |  input whole file    |
|   `$`    |  input last line     |
| `<num>`  |  input line `<num>`  |

## search

See:

```
:help /\c
:help /\C
:help 'smartcase'
```

## shell

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


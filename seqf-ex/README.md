# Simple `seq_file` example

This is a simpe `seq_file` example that will expose its functionality via `/proc/seqf-ex` file. Once the module has started, to see the output, type:

```shell
cat /proc/seqf-ex
```

You can check if the buffer of size 2048 is being printed with steps of 128 bytes (amounting to 16 lines):

```shell
awk 'BEGIN { line=0 } { line++; print "Line" OFS line OFS "length:" OFS length($0) } END { print "Line count:" OFS line }' /proc/seqf-ex
```

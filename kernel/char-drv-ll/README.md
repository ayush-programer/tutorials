# Character driver with linked list example

After running `make start`, you can try writing and reading from the device:

```shell
$ echo test > /dev/char-drv-ll-0
$ cat /dev/char-drv-ll-0
test
```


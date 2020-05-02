proj = netlink-test

ifeq ($(CC),cc)
	CC = gcc
endif

$(proj): $(proj).o
	$(CC) $(proj).o -o $(proj)

$(proj).o: $(proj).c
	$(CC) -c $(proj).c -o $(proj).o

.PHONY=run
run: $(proj)
	./$(proj)

.PHONY=clean
clean:
	rm -rf $(proj) $(proj).o


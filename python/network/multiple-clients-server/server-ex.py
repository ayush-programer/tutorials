# Python3 server example

import socket
import time
import selectors
import types

def accept_conn(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)

    print(
            "Accepted connection from: %s" %
            str(addr)
            )

    sel.register(
            conn,
            selectors.EVENT_READ | selectors.EVENT_WRITE,
            types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
            )

    return addr

def process_data(key, mask, addr, sel):
    sock = key.fileobj

    if mask & selectors.EVENT_READ:
        data = sock.recv(64)

        if data:
            print(
                    "Got message from %s: %s" %
                    (str(addr), data.decode("utf-8"))
                    )
            key.data.outb += data

        else:
            print(
                    "Closing connection to %s..." %
                    str(addr)
                    )
            sel.unregister(sock)
            sock.close()

    elif mask & selectors.EVENT_WRITE:

        if key.data.outb:
            key.fileobj.send(b"OK")
            key.data.outb = b""

def start_server(sock):

    while True:
        try:
            sock.bind(sock_addr)

        except OSError:
            print("Socket busy, retrying in 60s...")
            time.sleep(60)

            continue

        else:
            print("Socket bound to %s:%d." % sock_addr)

            break

    sock.listen() # number of clients
    print("Waiting for connections...")

    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, data=None)

    while True:
        events = sel.select(timeout=None)

        for key, mask in events:

            if key.data is None:
                addr = accept_conn(sock)
            else:
                process_data(key, mask, addr, sel)

sel = selectors.DefaultSelector()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock_addr=('127.0.0.1', 12000)

    try:
        start_server(sock)

    except KeyboardInterrupt:
        sock.close()

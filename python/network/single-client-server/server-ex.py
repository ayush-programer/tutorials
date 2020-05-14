# Python3 server example

import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    sock_addr=('127.0.0.1', 12000)

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

    sock.listen(1) # number of clients
    conn = None
    print("Waiting for connections...")

    while True:

        try:
            conn, addr = sock.accept()

            print("Accepted connection from: %s" % str(addr))

            while True:
                data = conn.recv(64)

                if not data:
                    break
                else:
                    print("Got message from %s: %s" % (str(addr), data.decode("utf-8")))
                    conn.sendall(b"OK")

        except KeyboardInterrupt:
            print("Received keyboard interrupt.")

            break

        finally:
            print("Closing connection.")

            if conn:
                conn.close()

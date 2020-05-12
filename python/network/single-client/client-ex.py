# Python3 Client Example

import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    server_address = ("127.0.0.1", 12000)

    try:
        sock.connect(server_address)
        user_input = None

        while user_input != "q":
            user_input = input("Type in a message (q to quit): ")

            if user_input != "q":
                user_bytes = bytes(user_input, "utf-8")
                sock.send(user_bytes)
                data = sock.recv(64)

                print("Server response: %s" % data.decode("utf-8"))

    except KeyboardInterrupt:
        print("You could have just typed 'q'")

    finally:
        print("Closing socket...")
        sock.close()

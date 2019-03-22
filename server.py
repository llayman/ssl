#  openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem

import socket
import ssl
import os

# change the following value to match your IP address
HOST = '152.20.196.150'
PORT = 40043

CERTIFICATE = os.path.join('secrets', 'certificate.pem')
PRIVATE_KEY = os.path.join('secrets', 'key.pem')


def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTIFICATE, keyfile=PRIVATE_KEY)

    with socket.socket() as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print("SERVER {} now listening for connection on port {}...".format(HOST, PORT))

        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                # The following line BLOCKS execution while listening for a connection
                conn, from_addr = ssock.accept()
                print("SERVER received message from {}: {}".format(from_addr, conn.recv(1024)))
                conn.write('Message acknowledged'.encode('utf-8'))


if __name__ == '__main__':
    main()

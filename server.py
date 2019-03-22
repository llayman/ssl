#  openssl req -newkey rsa:2048 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem

import socket, ssl
import os

HOST = '152.20.196.150'
PORT = 40043


CERTIFICATE = os.path.join('secrets', 'certificate.pem')
PRIVATE_KEY = os.path.join('secrets', 'key.pem')


def main():

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTIFICATE, keyfile=PRIVATE_KEY)

    bindsocket = socket.socket()
    bindsocket.bind((HOST, PORT))
    bindsocket.listen(5)
    print("SERVER {} now listening for connection on port {}...".format(HOST, PORT))

    while True:
        newsocket, fromaddr = bindsocket.accept()
        try:
            conn = context.wrap_socket(newsocket, server_side=True)
            print("SERVER received message from {}: {}".format(conn.getpeername()[0], conn.recv()))
            conn.write('Message acknowledged'.encode('utf-8'))
        except ssl.SSLError as e:
            print('SERVER ERROR:', e)
        finally:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()


if __name__ == '__main__':
    main()

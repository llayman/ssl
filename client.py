import argparse
import socket
import ssl
import os

parser = argparse.ArgumentParser(description='Send a message via SSL/TLS.')
parser.add_argument('host')
parser.add_argument('port', type=int)
parser.add_argument('message')

args = parser.parse_args()

context = ssl.create_default_context()
# Normally you would NOT do this, but we want to accept self-signed certificates without their public key in this case
context.check_hostname = False
# context.verify_mode = ssl.CERT_OPTIONAL
context.verify_mode = ssl.CERT_NONE
# context.load_verify_locations(os.path.join('secrets', 'certificate.pem'))

with socket.create_connection((args.host, args.port)) as sock:
    with context.wrap_socket(sock, server_hostname=args.host) as conn:
        print("CLIENT says: connection type:", conn.version())
        print("CLIENT says: server certificate:", conn.getpeercert())

        conn.sendall(args.message.encode('utf-8'))
        print("{}: {}".format(conn.getpeername()[0], conn.recv()))


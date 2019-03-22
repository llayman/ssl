from pprint import pprint
import argparse
import socket
import ssl

# HOST = '152.20.196.150'
# PORT = 40043

parser = argparse.ArgumentParser(description='Send a message via SSL/TLS.')
parser.add_argument('host')
parser.add_argument('port', type=int)
parser.add_argument('message')

args = parser.parse_args()

# context = ssl.create_default_context()
context = ssl._create_unverified_context()
# context = ssl.SSLContext()
# context.verify_mode = ssl.CERT_OPTIONAL
# context.check_hostname = False
# context.load_default_certs()

with socket.create_connection((args.host, args.port)) as sock:
    with context.wrap_socket(sock, server_hostname=args.host) as conn:
        print("CLIENT says: connection type:", conn.version())
        print("CLIENT says: server certificate:", conn.getpeercert())

        conn.sendall(args.message.encode('utf-8'))
        print("{}: {}".format(conn.getpeername()[0], conn.recv()))


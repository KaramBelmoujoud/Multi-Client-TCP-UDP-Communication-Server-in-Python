import socket
from time import sleep
import time


def main():
    ip = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0]+(".255")
    msg = b'response'

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            try:
                sock.sendto(msg, (ip, 5005))
            except:
                continue
            sock.close()
            sleep(1)


main()

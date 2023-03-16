import socket
from inputimeout import inputimeout


def tcpp():
    while True:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            clientSocket.connect((addr[0], 9090))
            while True:
                try:
                    data = inputimeout(prompt='', timeout=5)
                    clientSocket.send(data.encode())
                except:
                    clientSocket.close()
                    break
        except:
            break
        break
    return 0


while True:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 5005))
    while True:
        data, addr = sock.recvfrom(1024)
        resp = b'response'
        if (data == resp):
            tcpp()

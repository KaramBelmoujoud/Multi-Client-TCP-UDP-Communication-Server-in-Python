import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(("0.0.0.0", 9090))
serverSocket.listen()
while (True):
    (clientConnected, clientAddress) = serverSocket.accept()
    print("Accepted a connection request from %s:%s" %
          (clientAddress[0], clientAddress[1]))

    while True:
        try:
            dataFromClient = clientConnected.recv(1024)
            print(dataFromClient.decode())
            clientConnected.send("h".encode())
        except:
            break

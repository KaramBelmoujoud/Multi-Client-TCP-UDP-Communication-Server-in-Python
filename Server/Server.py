import socket
import pyautogui
import pydirectinput
from time import sleep
import time
import threading
lock = threading.Lock()


def send_IP():
    ip = socket.gethostbyname(
        socket.gethostname()).rsplit('.', 1)[0]+(".255")
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


def get_CMD():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", 9090))
    serverSocket.listen()
    serverSocket.settimeout(3)
    while True:
        try:
            (clientConnected, clientAddress) = serverSocket.accept()
            print("Accepted a connection request from %s:%s" %
                  (clientAddress[0], clientAddress[1]))
            while True:
                try:
                    dataFromClient = clientConnected.recv(1024)
                    msg = dataFromClient.decode()

                    if msg.rsplit('(', 1)[0] == "move":
                        pydirectinput.moveTo(int(msg[5:].rsplit(',', 1)[0]), int(
                            msg[5:-1].rsplit(',', 1)[1]))
                    elif msg == "left":
                        pydirectinput.press("left")
                        print(msg)
                    elif msg == "right":
                        pydirectinput.press("right")
                    elif msg == "up":
                        pydirectinput.press("up")
                    elif msg == "down":
                        pydirectinput.press("down")
                    elif msg == "click":
                        pydirectinput.click()
                    clientConnected.send("h".encode())
                except:
                    break
        except:
            print("Waiting for a connection request")
            continue


thread1 = threading.Thread(target=send_IP, args=())
thread2 = threading.Thread(target=get_CMD, args=())
# Starting the threads
thread1.start()
thread2.start()
# Waiting for the threads to finish
thread1.join()
thread2.join()

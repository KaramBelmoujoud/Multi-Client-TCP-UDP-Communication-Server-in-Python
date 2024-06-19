import socket
from time import sleep
import threading

def send_ip():
    broadcast_ip = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0] + ".255"
    msg = b'response'
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        try:
            udp_socket.sendto(msg, (broadcast_ip, 5005))
            sleep(1)
        except Exception as e:
            print(f"Error broadcasting IP: {e}")

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_address} disconnected")
                break
            msg = data.decode()
            print(f"Received from {client_address}: {msg}")
            client_socket.send("h".encode())
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_address} closed")

def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 9090))
    server_socket.listen()
    print("TCP server listening on port 9090")
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except Exception as e:
            print(f"Error accepting connections: {e}")

if __name__ == "__main__":
    udp_thread = threading.Thread(target=send_ip)
    tcp_thread = threading.Thread(target=tcp_server)
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

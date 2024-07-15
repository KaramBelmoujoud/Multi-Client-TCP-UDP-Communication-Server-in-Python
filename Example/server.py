import socket
from time import sleep
import threading
from concurrent.futures import ThreadPoolExecutor
import ssl
import os

MAX_THREADS = 10  # Maximum number of concurrent client threads

# Determine the script's directory and set paths to the certificate and key files
script_dir = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(script_dir, 'server.crt')
KEY_FILE = os.path.join(script_dir, 'server.key')

# Check if certificate and key files exist
if not os.path.isfile(CERT_FILE) or not os.path.isfile(KEY_FILE):
    raise FileNotFoundError(f"Certificate or key file not found: {CERT_FILE}, {KEY_FILE}")

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
    client_socket.settimeout(60)  # Set timeout for client socket
    try:
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print(f"Client {client_address} disconnected")
                    break
                msg = data.decode()
                print(f"Received from {client_address}: {msg}")
                client_socket.send("h".encode())
            except socket.timeout:
                print(f"Client {client_address} timed out")
                break
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

    # Wrap the socket with SSL
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    server_socket = context.wrap_socket(server_socket, server_side=True)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                executor.submit(handle_client, client_socket, client_address)
            except Exception as e:
                print(f"Error accepting connections: {e}")

if __name__ == "__main__":
    udp_thread = threading.Thread(target=send_ip)
    tcp_thread = threading.Thread(target=tcp_server)
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

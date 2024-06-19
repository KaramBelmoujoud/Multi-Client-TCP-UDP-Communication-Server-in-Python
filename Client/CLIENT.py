import socket
from inputimeout import inputimeout, TimeoutOccurred

def tcpp(addr):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((addr[0], 9090))
        print(f"Connected to server at {addr[0]}:9090")
        while True:
            try:
                data = inputimeout(prompt='', timeout=5)
                client_socket.send(data.encode())
            except TimeoutOccurred:
                continue
            except Exception as e:
                print(f"Error sending data: {e}")
                break
    except Exception as e:
        print(f"Error connecting to server: {e}")
    finally:
        client_socket.close()
        print("Connection closed, waiting for new server broadcast")

def udp_listener():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.bind(("0.0.0.0", 5005))
    print("Listening for server broadcast on port 5005")
    while True:
        try:
            data, addr = udp_socket.recvfrom(1024)
            if data == b'response':
                tcpp(addr)
        except Exception as e:
            print(f"Error receiving UDP broadcast: {e}")

if __name__ == "__main__":
    udp_listener()

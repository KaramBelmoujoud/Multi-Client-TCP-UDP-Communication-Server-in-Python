# Network Package

This package provides a client-server communication system using TCP and UDP With SSL/TLS security Certification.

## Installation

To install the package, run:

```bash
pip install network_com
```

## Generating SSL Certificates

To use SSL/TLS with this package, you need to generate SSL certificates. For development purposes, you can create self-signed certificates using OpenSSL:

### Generate a Private Key

```bash
openssl genpkey -algorithm RSA -out server.key
```

### Generate a Certificate Signing Request (CSR)

```bash
openssl req -new -key server.key -out server.csr -subj "/CN=example.com"
```

###Generate a Self-Signed Certificate

```bash
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```

You will have server.key and server.crt files to be used by the server.

## Using OpenSSL

### Install OpenSSL

If you don't already have OpenSSL installed, you can install it:

### On Ubuntu:

```bash
sudo apt-get install openssl
```

### On macOS (using Homebrew):

```bash
brew install openssl
```

### On Windows:

Download and install from OpenSSL for Windows.

## Usage

### Running the Server

To start the server, you can start the server using the package in your own script:

```python
# my_server_script.py

from network_com import server
import threading
import os

def start_server():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    udp_thread = threading.Thread(target=server.send_ip)
    tcp_thread = threading.Thread(target=server.tcp_server, args=(os.path.join(script_dir, 'server.crt'), os.path.join(script_dir, 'server.key')))
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

if __name__ == "__main__":
    start_server()

```

Run the script with:

```bash
python my_server_script.py
```

### Running the Client

To start the client, you can start the client using the package in your own script:

```python
# my_client_script.py

from network_com import client
import os

def start_client():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    client.udp_listener(os.path.join(script_dir, 'server.crt'))

if __name__ == "__main__":
    start_client()
```

Run the script with:

```bash
python my_script.py
```

## Combined Example

Here is an example script (combined_script.py) that allows you to run either the client or the server based on a command-line argument:

```python
# combined_script.py

from network_com import client, server
import threading
import argparse

def start_client(certfile):
    client.udp_listener(certfile)

def start_server(certfile, keyfile):
    udp_thread = threading.Thread(target=server.send_ip)
    tcp_thread = threading.Thread(target=server.tcp_server, args=(certfile, keyfile))
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run network client or server.")
    parser.add_argument('mode', choices=['client', 'server'], help="Mode to run: client or server")
    parser.add_argument('--certfile', required=True, help="Path to the SSL certificate file")
    parser.add_argument('--keyfile', help="Path to the SSL key file (required for server)")

    args = parser.parse_args()

    if args.mode == 'client':
        start_client(args.certfile)
    elif args.mode == 'server':
        if not args.keyfile:
            parser.error("The --keyfile argument is required for running the server")
        start_server(args.certfile, args.keyfile)

```

Run the script with:

```bash
# To start the server
python combined_script.py server --certfile path/to/server.crt --keyfile path/to/server.key

# To start the client
python combined_script.py client --certfile path/to/server.crt
```

## Using the Package in Other Projects

You can import and use the package in any other Python project. Here’s an example:

```python
# another_script.py

from network_com import client, server
import threading

def main():
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server, args=(os.path.join(script_dir, 'server.crt'), os.path.join(script_dir, 'server.key')))
    server_thread.start()

    # Start client in the main thread (or another separate thread if desired)
    start_client("path/to/server.crt")

def start_server(certfile, keyfile):
    udp_thread = threading.Thread(target=server.send_ip)
    tcp_thread = threading.Thread(target=server.tcp_server, args=(certfile, keyfile))
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

def start_client(certfile):
    client.udp_listener(certfile)

if __name__ == "__main__":
    main()

```

Run the script with:

```bash
python another_script.py
```

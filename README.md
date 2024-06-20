# Network Package

This package provides a client-server communication system using TCP and UDP.

## Installation

To install the package, run:

```bash
pip install .
```

## Usage

### Running the Server

To start the server, you can use the provided run-server command:

```bash
run-server
```

Alternatively, you can start the server using the package in your own script:

```python
# my_script.py

from my_network_package import server
import threading

def start_server():
    udp_thread = threading.Thread(target=server.send_ip)
    tcp_thread = threading.Thread(target=server.tcp_server)
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

if __name__ == "__main__":
    start_server()
```

Run the script with:

```bash
python my_script.py
```

### Running the Client

To start the client, you can use the provided run-client command:

```bash
run-client
```

Alternatively, you can start the client using the package in your own script:

```python
# my_script.py

from my_network_package import client

def start_client():
    client.udp_listener()

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

from my_network_package import client, server
import threading
import argparse

def start_client():
    client.udp_listener()

def start_server():
    udp_thread = threading.Thread(target=server.send_ip)
    tcp_thread = threading.Thread(target=server.tcp_server)
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run network client or server.")
    parser.add_argument('mode', choices=['client', 'server'], help="Mode to run: client or server")

    args = parser.parse_args()

    if args.mode == 'client':
        start_client()
    elif args.mode == 'server':
        start_server()
```

Run the script with:

```bash
# To start the server
python combined_script.py server

# To start the client
python combined_script.py client
```

## Using the Package in Other Projects

You can import and use the package in any other Python project. Here’s an example:

```python
# another_script.py

from my_network_package import client, server
import threading

def main():
    # Start server in a separate thread
    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    # Start client in the main thread (or another separate thread if desired)
    start_client()

def start_server():
    udp_thread = threading.Thread(target=server.send_ip)
    tcp_thread = threading.Thread(target=server.tcp_server)
    udp_thread.start()
    tcp_thread.start()
    udp_thread.join()
    tcp_thread.join()

def start_client():
    client.udp_listener()

if __name__ == "__main__":
    main()
```

Run the script with:

```bash
python another_script.py
```

## License

This project is licensed under the GNU General Public License v3.0.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

```perl
This `README.md` now correctly reflects the use of the GPL-3.0 license. Make sure to include the full license text in your repository, typically in a file named `LICENSE`.
```

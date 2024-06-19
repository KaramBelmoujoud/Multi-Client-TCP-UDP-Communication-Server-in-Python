## Description

This project showcases a Python-based server capable of managing multiple client connections concurrently, utilizing a combination of TCP and UDP protocols. The server broadcasts its presence via UDP, allowing clients to discover it on the network. Once discovered, clients establish a TCP connection to the server, enabling robust and efficient communication.

## Key Features

- **UDP Broadcasting for Discovery:** The server periodically broadcasts a message over UDP to inform potential clients of its presence on the network.
- **Multi-Client TCP Handling:** Using Python's threading module, the server can handle multiple clients simultaneously, ensuring responsive and scalable interactions.
- **Timeout and Exception Handling:** Both client and server implementations include comprehensive timeout and exception handling to ensure stability and reliability.
- **Simple Communication Protocol:** Clients send messages to the server, which acknowledges receipt, demonstrating a basic request-response protocol.

## Detailed Explanation

### Server Code

1. **send_ip Function:**

   - Broadcasts the server's presence on the local network using UDP.
   - Constructs a broadcast IP address and sends a predefined message (`b'response'`) every second.

2. **handle_client Function:**

   - Manages communication with a single client.
   - Receives messages from the client, prints them, and sends back an acknowledgment ("h").

3. **tcp_server Function:**

   - Listens for incoming TCP connections on port 9090.
   - For each connection, spawns a new thread running `handle_client` to manage the interaction with that client, allowing the server to handle multiple clients concurrently.

4. **Main Execution:**
   - Starts two threads: one for broadcasting the server's presence (`send_ip`) and another for accepting and managing TCP connections (`tcp_server`).

### Client Code

1. **tcpp Function:**

   - Creates a TCP client socket and attempts to connect to the server on port 9090.
   - Reads user input with a timeout, sending the input to the server over the established TCP connection.

2. **udp_listener Function:**

   - Listens for UDP broadcast messages from the server on port 5005.
   - Upon receiving the broadcast message (`b'response'`), initiates the TCP connection by calling `tcpp`.

3. **Main Execution:**
   - Runs the `udp_listener` function, enabling the client to discover the server via UDP and then communicate with it over TCP.

## Getting Started

### Prerequisites

- Python 3.x
- `inputimeout` library (install via `pip install inputimeout`)

### Running the Server

```bash
python server.py
```

### Running the Client

```bash
python server.py
```

### Example Usage:

1. **Start the server:**

```bash
python server.py
```

2. **Start one or more clients:**

```bash

python client.py
```

3. **Enter messages in the client terminal to send them to the server.**

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your improvements.

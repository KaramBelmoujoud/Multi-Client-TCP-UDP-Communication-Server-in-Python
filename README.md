## This a TCP communition project with two different machines in the same Network using Python 

### Server side:

The Server side is gonna be running two different Codes :

- UDP_Server.py is used to send the Server IP to the client to establish a communication;
- TCP_Server.py is used to Connect and establish communication with Client to send and receive Sockets(continuous commincation messages)

The order of running doesn't matter

### Client side:

The Client side code has a mix of UDP and TCP:

- Client.py is used to receive at first the machines IP from the UDP_Server.py which then make the Client communicate with Server's Ip Address and establish the communication and send msg to the server as an input 


### NOTE:

Order of running the scripts doesn't matter you can run in what ever order you please even after an interuption

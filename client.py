import threading
import sys
import socket 

## Client.py
s = socket.socket()
host = input(str("Please enter the hostname of the server: "))
port = 9999
s.connect((host, port))
print("Connected to chat server.")

## Open a socket, connect to the server of the users choice at port 9999.
name = input(str("Please enter your name: "))
s.send(name.encode('ascii'))

## Get the Clients name and send it to the server.
def receive():
    while True:
        message = s.recv(1024)
        message = message.decode('ascii')
        print(message)

## Create a new thread for receiving messages from the server.
threading.Thread(target=receive).start()

## Send messages to the server
while True:
    message = input(str(">> "))
    message = message.encode('ascii')
    s.send(message)

## Receive messages from the server.
def receive():
    while True:
        message = s.recv(1024)
        message = message.decode('ascii')
        print(message)

## Create a new thread for receiving messages from the server.
threading.Thread(target=receive).start()

## When the user connects to the server, take their first message and set it as their name.
name = conn.recv(1024)
name = name.decode('ascii')
print("Connected with " + name)



import threading
import sys
import socket 
import os

## Client.py
s = socket.socket()
host = input(str("Please enter the hostname of the server: "))
port = 9999
s.connect((host, port))
os.system("title Chat room connected at " + host)
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



## Check each message from the server, and collect the text stored in the beginning surrounded by <> and put it into an array called "Users"
while True:
    message = conn.recv(1024)
    message = message.decode('ascii')
    if "<" in message:
        message = message.split("<")
        message = message[1].split(">")
        Users.append(message[0])


print("Connected with " + name)

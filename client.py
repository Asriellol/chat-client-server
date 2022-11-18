import socket
import sys
import threading
import time

## Open a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

## Connect to the server 
s.connect(('127.0.0.1', 9999))

## Get the client's name and send it to the server 
name = input("Enter your name: ") 
s.send(name.encode('utf-8')) 


## Function to handle messages received from the server 
def receiveMessages(): 

    while True: 

        try: 

            message = s.recv(1024).decode('utf-8')  

            print(message)  

        except:  

            continue  

        
## Create a new thread for receiving messages from the server 
threading._start_new_thread(receiveMessages, ())  

        
## Send messages to the server and exit when the user types "exit" 
while True:  

    message = input()  

    if message == "exit":  

        s.send("exit".encode('utf-8'))  

        s.close()  

        sys.exit()  

    else:  

        s.send(message.encode('utf-8'))

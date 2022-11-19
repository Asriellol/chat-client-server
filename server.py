import socket
import sys
import threading
import time
import datetime

## Open a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

## Bind the socket to a port and listen for connections
s.bind(("0.0.0.0", 9999))
s.listen(5)
print("Server is listening...")
print("Server address: {}".format(socket.gethostbyname(socket.gethostname())))

## Create a list of clients that are connected to the server
clients = []


## Function to handle incoming connections from clients
def handleClient(client):

    ## Get the client's name and send a welcome message to them
    name = client.recv(1024).decode('utf-8')
    client.send("Welcome to the chat room! \nYou can type exit to leave!".encode('utf-8'))

    ## Add the client to the list of clients connected to the server and broadcast their connection to all other clients in the chat room
    clients.append(client)

    while True:

        ## Receive messages from clients and broadcast them to all other clients in the chat room 
        try: 

            message = client.recv(1024).decode('utf-8')

            if message == "User has disconnected": 

                ## Remove the client from the list of clients connected to the server and broadcast their disconnection to all other clients in the chat room 
                index = clients.index(client) 

                del clients[index] 

                print("Client has disconnected") 

                break 

            else: 

                print("{} : {}".format(name, message)) 

                for c in clients: 

                    with open("log.txt", "a") as f:
                        f.write("{} : {}".format(name, message))
                        f.write("\n")
                        f.close()
                    c.send("{} : {}".format(name, message).encode('utf-8')) 

        except: 

            continue 

    client.close() 

    
## Accept incoming connections from clients and create a new thread for each one that connects  
while True: 

    try:  

        client, address = s.accept()  

        print("Connected with {}".format(str(address)))  

        threading._start_new_thread(handleClient, (client,))  

    except KeyboardInterrupt:  

        s.close()  

        sys.exit()

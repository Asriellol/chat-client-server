import socket
import threading
import sys
import random

def main():
    # Open a socket and bind it to 0.0.0.0, 9999 then listen for connections and print the server address and port to the terminal.
    s = socket.socket()
    host = "0.0.0.0"
    port = 9999
    s.bind((host, port))
    s.listen(10)
    print("Server is now listening on " + host + ":" + str(port))

    # Accept connections, and Create a list of all the clients that connect to the server.
    clients = []
    disconnected = []
    messages = []
    def clientThread(conn, addr):
        name = conn.recv(1024)
        name = name.decode('ascii')
        print(name + " connected.")
        broadcast(name + " connected.", conn)
        for message in messages:
            conn.send(message.encode('ascii'))
        # Create a loop, that receives messages from clients and broadcasts them to all other users.
        while True:
            try:
                message = conn.recv(1024)
                message = message.decode('ascii')
                if message:
                    print("<" + name + "> " + message)
                    message_to_send = "<" + name + "> " + message
                    messages.append(message_to_send)
                    if len(messages) > 20:
                        messages.pop(0)
                    broadcast(message_to_send, conn)
                else:
                    remove(conn)
                    print(name + " disconnected.")
            except ConnectionResetError:
                print(name + " disconnected.")
                if name not in disconnected:
                    broadcast(name + " disconnected.", conn)
                    disconnected.append(name)
                else:
                    print("User disconnected numerous times in a row.")
                remove(conn)
                break

    # Broadcast the connection of the new user to all other users in the chat room.
    def broadcast(message, connection):
        for client in clients:
            if client != connection:
                try:
                    client.send(message.encode('ascii'))
                except:
                    client.close()
                    remove(client)


    ## Remove the client from the list of clients.
    def remove(connection):
        if connection in clients:
            clients.remove(connection)


    ## Create a loop, that receives messages from clients and broadcasts them to all other users. Then start a new thread for each client that connects to the server.
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        print(str(addr[0]) + " connected.")
        threading.Thread(target=clientThread, args=(conn, addr)).start()

if __name__ == "__main__":
    main()

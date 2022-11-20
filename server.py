import socket
import threading
import sys
import os

def main():
    # Open a socket and bind it to 0.0.0.0, 9999 then listen for connections and print the server address and port to the terminal. Then create a list of all the clients that connect to the server.
    s = socket.socket()
    host = "0.0.0.0"
    port = 9999
    s.bind((host, port))
    s.listen(10)
    print("Server is now listening on " + host + ":" + str(port))

    clients = []
    # If the file chat_history.txt exists, then open it and read the messages.
    if os.path.exists("chat_history.txt"):
        file = open("chat_history.txt", "r")
        messages = file.readlines()
        file.close()
    # If the file chat_history.txt does not exist, then create it and write the messages to it.
    else:
        file = open("chat_history.txt", "w")
        messages = []
        file.close()
        # Receive the name of the client and print it to the terminal.
    def clientThread(conn, addr):
        name = conn.recv(1024)
        name = name.decode('ascii')
        print(name + " connected.")
        # Broadcast the connection of the new user to all other users in the chat room.
        broadcast(name + " connected.", conn)
        # Send the last 20 messages to the client.
        for message in messages:
            conn.send((message + "\n").encode('ascii'))
        # Create a loop, that receives messages from clients and broadcasts them to all other users. Then start a new thread for each client that connects to the server.
        while True:
            try:
                # Receive the message from the client.
                message = conn.recv(1024)
                message = message.decode('ascii')
                # If the message is not empty, then broadcast it to all other users.
                if message:
                    print("<" + name + "> " + message)
                    message_to_send = "<" + name + "> " + message
                    messages.append(message_to_send)
                    # Write the message to the file chat_history.txt.
                    file = open("chat_history.txt", "a")
                    file.write(message_to_send)
                    file.close()
                    # If the list of messages is longer than 20, then remove the oldest message.
                    if len(messages) > 20:
                        messages.pop(0)
                    broadcast(message_to_send, conn)
                # If the message is empty, then remove the client from the list of clients and print that they disconnected.
                else:
                    remove(conn)
                    print(name + " disconnected.")
            # If the client disconnects, then print that they disconnected.
            except ConnectionResetError:
                print(name + " disconnected.")
                broadcast(name + " disconnected.", conn)
                remove(conn)
                break

                break

    # Broadcast the message to all other users in the chat room.
    def broadcast(message, connection):
        for client in clients:
            if client != connection:
                try:
                    client.send(message.encode('ascii'))
                except:
                    client.close()
                    remove(client)

    # Remove the client from the list of clients.
    def remove(connection):
        if connection in clients:
            clients.remove(connection)
    # Create a loop, that receives messages from clients and broadcasts them to all other users. Then start a new thread for each client that connects to the server.
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        print(str(addr[0]) + " connected.")
        threading.Thread(target=clientThread, args=(conn, addr)).start()

if __name__ == "__main__":
    main()

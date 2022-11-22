import socket
import sys
import time
import os
import threading
import random
import string
import hashlib
import base64
import json
from PIL import Image
from io import BytesIO
from Crypto.Cipher import AES
from Crypto import Random


## Global Variables ##

# Server Variables #
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 9999))
server.listen(5)


# Client Variables #
clients = []


## Functions ## 
def send_message(message):
    for client in clients: 
        client.send(message) 
        

        
def send_message_to_client(message, client):
    client.send(message)


def send_message_to_all_clients(message):
    for client in clients:
        client.send(message)


def send_message_to_all_clients_except(message, client):
    for c in clients:
        if c != client:
            c.send(message)


def send_image(image):
    for client in clients: 
        client.send(image) 


def send_image_to_client(image, client):
    client.send(image)


def send_image_to_all_clients(image):
    for client in clients: 
        client.send(image) 


def send_image_to_all_clients_except(image, client):
    for c in clients: 
        if c != client: 
            c.send(image) 

            
def send_color(color):
    for client in clients: 
        client.send(color) 

        
def send_color_to_client(color, client):
    client.send(color)

    
def send_color_to_all_clients(color):
    for client in clients: 
        client.send(color) 

        
def send_color_to_all_clients_except(color, client):
    for c in clients: 
        if c != client: 
            c.send(color) 

            
def getRandomString():  # Generates a random string of letters and digits and returns the string. Used for generating passwords. 
    lettersAndDigits = string.ascii_letters + string.digits  # All letters and digits 
    return ''.join((random.choice(lettersAndDigits) for i in range(20)))  # Join method is used to combine a string and an iterable and returns a string.

    
def getRandomNumber(): # Generates a random number between 1 and 100 and returns the number. Used for generating usernames. 
    return random.randint(1, 100)

    
def getRandomColor(): # Generates a random color in hex and returns the value. Used for generating colors. 
    return '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    
def getRandomImage(): # Generates a random image and returns the image object. Used for generating profile pictures. 
    image = Image.new('RGB', (100, 100)) # Create a new black image 
    pixels = image.load() # Create the pixel map 

    for i in range(image.size[0]): # For every pixel: 
        for j in range(image.size[1]): 
            pixels[i, j] = (i, j, 100) # Set the colour accordingly  

    return image

    
def encryptMessageAES(message, key): # Encrypts a message using AES encryption and returns the encrypted message as bytes object. Used to encrypt messages before sending them to the server or other clients to prevent eavesdropping or tampering with messages while they are being sent over the network.  

    iv = Random.new().read(AES.block_size) # Generate initialization vector (IV). The IV is used to ensure that the same message encrypted with the same key does not produce the same ciphertext output every time it is encrypted (this would make it easier to break the encryption). The IV is sent along with the ciphertext so that the receiver can decrypt it properly using the same IV that was used to encrypt it in the first place (the IV does not need to be kept secret).  

    cipher = AES.new(key, AES.MODE_CFB, iv) # Create a new AES cipher object using CFB mode (Cipher Feedback Mode). CFB mode is similar to CBC mode except that instead of XORing each block of plaintext with the previous ciphertext block before encrypting it, it XORs each block of plaintext with the previous ciphertext block after encrypting it (this makes it more secure than CBC mode).  

    return base64.b64encode((iv + cipher.encrypt(message))) # Encode the IV and ciphertext as base64 and return them as bytes object (the IV is prepended to the ciphertext so that they can be sent together).  

    
def decryptMessageAES(ciphertext, key): # Decrypts an AES encrypted message and returns the decrypted message as bytes object (the IV is prepended to the ciphertext so that they can be sent together). Used to decrypt messages received from other clients or from the server after they have been encrypted using AES encryption to prevent eavesdropping or tampering with messages while they are being sent over the network (the IV is prepended to the ciphertext so that they can be sent together).  

    ciphertext = base64.b64decode(ciphertext) # Decode the base64 encoded IV and ciphertext as bytes object (the IV is prepended to the ciphertext so that they can be sent together).  

    iv = ciphertext[:AES.block_size] # Get initialization vector (IV). The IV is used to ensure that the same message encrypted with the same key does not produce the same ciphertext output every time it is encrypted (this would make it easier to break the encryption). The IV is sent along with the ciphertext so that the receiver can decrypt it properly using the same IV that was used to encrypt it in the first place (the IV does not need to be kept secret).  

    cipher = AES.new(key, AES.MODE_CFB, iv) # Create a new AES cipher object using CFB mode (Cipher Feedback Mode). CFB mode is similar to CBC mode except that instead of XORing each block of plaintext with the previous ciphertext block before encrypting it, it XORs each block of plaintext with the previous ciphertext block after encrypting it (this makes it more secure than CBC mode).  

    return cipher.decrypt((ciphertext[AES.block_size:])) # Decrypt and return the message as bytes object (the IV is prepended to the ciphertext so that they can be sent together).  

    
def hashPasswordSHA256(password): # Hashes a password using SHA256 hashing algorithm and returns its hash as bytes object (SHA256 produces a 256 bit hash which is 32 bytes long). Used to hash passwords before storing them in database so that if someone gains access to database they will not be able to see users' passwords since they will be hashed (hashing is one way process which means you cannot get back original password from its hash).  

    return hashlib.sha256((password + 'salt').encode('utf-8')).digest() # Hash password using SHA256 hashing algorithm and return its hash as bytes object (SHA256 produces a 256 bit hash which is 32 bytes long). The salt is added at end of password before hashing it so that even if two users have same password their hashes will still be different since salt will be different for each user (this makes it harder for an attacker who gains access to database to crack users' passwords since he will not know what salt was used when hashing each password).  

    
class ClientThread: # Client thread class which handles all communication between server and individual clients connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

    def __init__(self, ip, port, conn): # Constructor method which initializes instance variables when instance of this class is created by server thread class when new connection between server and individual client is established through sockets (each instance of this class represents one connection between server and one individual client).  

        self._ip = ip # IP address of individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

        self._port = port # Port number of individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

        self._conn = conn # Connection socket between server and individual client connected through sockets (each instance of this class represents one connection between server and one individual client).  

        self._username = '' # Username of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

        self._password = '' # Password of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

        self._color = '' # Color hex value of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

        self._profilePicture = None # Profile picture image object of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

        self._key = None 
        
        self._isLoggedIn = False # Boolean value which indicates whether individual user connected through sockets is logged in or not (each instance of this class represents one connection between server and one individual user).  

        self._isRegistered = False # Boolean value which indicates whether individual user connected through sockets is registered or not (each instance of this class represents one connection between server and one individual user).  

        self._isAdmin = False # Boolean value which indicates whether individual user connected through sockets is admin or not (each instance of this class represents one connection between server and one individual user).  

        self._isBanned = False # Boolean value which indicates whether individual user connected through sockets is banned or not (each instance of this class represents one connection between server and one individual user).  

        self._isMuted = False # Boolean value which indicates whether individual user connected through sockets is muted or not (each instance of this class represents one connection between server and one individual user).  

        self._isKicked = False # Boolean value which indicates whether individual user connected through sockets is kicked or not (each instance of this class represents one connection between server and one individual user).  

        self._isDisconnected = False # Boolean value which indicates whether individual user connected through sockets is disconnected or not (each instance of this class represents one connection between server and one individual user).  

        self._isThreadRunning = True # Boolean value which indicates whether thread for individual client connected to server through sockets is running or not (each instance of this class represents one connection between server and one individual client).  

        self._thread = threading.Thread(target=self.run) # Thread for individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

        self._thread.start() # Start thread for individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

    def run(self): # Run method for thread for individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

        while self._isThreadRunning: # While thread for individual client connected to server through sockets is running:  

            try: 
                data = self._conn.recv(1024) 
                if data: 
                    data = data.decode('utf-8') 
                    if data == 'exit': 
                        send_message_to_all_clients('{} has left the chat.'.format(self._username)) 
                        print('{} has left the chat.'.format(self._username)) 
                        clients.remove(self._conn) 
                        self._conn.close() 
                        break 
                    else: 
                        print('{}: {}'.format(self._username, data)) 
                        send_message_to_all_clients('{}: {}'.format(self._username, data)) 
            except: 
                continue 

    def getIP(self): # Getter method which returns IP address of individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

        return self._ip # Return IP address of individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

    def getPort(self): # Getter method which returns port number of individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

        return self._port # Return port number of individual client connected to server through sockets (each instance of this class represents one connection between server and one individual client).  

    def getConnection(self): # Getter method which returns connection socket between server and individual client connected through sockets (each instance of this class represents one connection between server and one individual client).  

        return self._conn # Return connection socket between server and individual client connected through sockets (each instance of this class represents one connection between server and one individual client).  

    def getUsername(self): # Getter method which returns username of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

        return self._username # Return username of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

    def setUsername(self, username): # Setter method which sets username of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

        self._username = username # Set username of individual user connected through sockets (each instance of this class represents one connection between server and one individual user).  

    def getPassword(self): # Getter method which returns password hash of individual user connected through sockets as bytes object (each instance of this class represents one connection between server and one individual user).  

        return self._password # Return password hash of individual user connected through sockets as bytes object (each instance of this class represents one connection between server and one individual user).  

    def setPassword(self, password): # Setter method which sets password hash of individual user connected through sockets as bytes object (each instance of this class represents one connection between server and one individual user).  

        self._password = password # Set password hash of individual user connected through sockets as bytes object (each instance of this class represents one connection between server and one individual user).  

    def getColor(self): # Getter method which returns color hex value of individual user connected through sockets as string object (each instance of this class represents one connection between server and one individual user).  

        return self._color # Return color hex value of individual user connected through sockets as string object (each instance of this class represents one connection between server and one individual user).  

    def setColor(self, color): # Setter method which sets color hex value of individual user connected through sockets as string object (each instance of this class represents one connection between server and one individual user).  

        self._color = color # Set color hex value of individual user connected through sockets as string object (each instance of this class represents one connection between server and one individual user).  

    def getProfilePicture(self):
        return self._profilePicture

    def setProfilePicture(self, profilePicture):
        self._profilePicture = profilePicture

    def getKey(self):
        return self._key

    def setKey(self, key):
        self._key = key

    def getIsLoggedIn(self): # Getter method which returns boolean value which indicates whether individual user connected through sockets is logged in or not (each instance of this class represents one connection between server and one individual user).  

        return self._isLoggedIn # Return boolean value which indicates whether individual user connected through sockets is logged in or not (each instance of this class represents one connection between server and one individual user).  

    def setIsLoggedIn(self, isLoggedIn): # Setter method which sets boolean value which indicates whether individual user connected through sockets is logged in or not (each instance of this class represents one connection between server and one individual user).  

        self._isLoggedIn = isLoggedIn # Set boolean value which indicates whether individual user connected through sockets is logged in or not (each instance of this class represents one connection between server and one individual user).  

    def getIsRegistered(self): # Getter method which returns boolean value which indicates whether individual user connected through sockets is registered or not (each instance of this class represents one connection between server and one individual user).  

        return self._isRegistered # Return boolean value which indicates whether individual user connected through sockets is registered or not (each instance of this class represents one connection between server and one individual user).  

    def setIsRegistered(self, isRegistered): # Setter method which sets boolean value which indicates whether individual user connected through sockets is registered or not (each instance of this class represents one connection between server and one individual user).  

        self._isRegistered = isRegistered # Set boolean value which indicates whether individual user connected through sockets is registered or not (each instance of this class represents one connection between server and one individual user).  

    def getIsAdmin(self): # Getter method which returns boolean value which indicates whether individual user connected through sockets is admin or not (each instance of this class represents one connection between server and one individual user).  

        return self._isAdmin # Return boolean value which indicates whether individual user connected through sockets is admin or not (each instance of this class represents one connection between server and one individual user).  

    def setIsAdmin(self, isAdmin): # Setter method which sets boolean value which indicates whether individual user connected through sockets is admin or not (each instance of this class represents one connection between server and one individual user).  

        self._isAdmin = isAdmin # Set boolean value which indicates whether individual user connected through sockets is admin or not (each instance of this class represents one connection between server and one individual user).  

    def getIsBanned(self): # Getter method which returns boolean value which indicates whether individual user connected through sockets is banned or not (each instance of this class represents one connection between server and one individual user).  

        return self._isBanned # Return boolean value which indicates whether individual user connected through sockets is banned or not (each instance of this class represents one connection between server and one individual user).  

    def setIsBanned(self, isBanned): # Setter method which sets boolean value which indicates whether individual user connected through sockets is banned or not (each instance of this class represents one connection between server and one individual user).  

        self._isBanned = isBanned # Set boolean value which indicates whether individual user connected through sockets is banned or not (each instance of this class represents one connection between server and one individual user).  

    def getIsMuted(self): # Getter method which returns boolean value which indicates whether individual user connected through sockets is muted or not (each instance of this class represents one connection between server and one individual user).  

        return self._isMuted # Return boolean value which indicates whether individual user connected through sockets is muted or not (each instance of this class represents one connection between server and one individual user).  

    def setIsMuted(self, isMuted): # Setter method which sets boolean value which indicates whether individual user connected through sockets is muted or not (each instance of this class represents one connection between server and one individual user).  

        self._isMuted = isMuted # Set boolean value which indicates whether individual user connected through sockets is muted or not (each instance of this class represents one connection between server and one individual user).  

    def getIsKicked(self): # Getter method which returns boolean value which indicates whether individual user connected through sockets is kicked or not (each instance of this class represents one connection between server and one individual user).  

        return self._isKicked # Return boolean value which indicates whether individual user connected through sockets is kicked or not (each instance of this class represents one connection between server and one individual user).  

    def setIsKicked(self, isKicked): # Setter method which sets boolean value which indicates whether individual user connected through sockets is kicked or not (each instance of this class represents one connection between server and one individual user).  

        self._isKicked = isKicked # Set boolean value which indicates whether individual user connected through sockets is kicked or not (each instance of this class represents one connection between server and one individual user).  

    def getIsDisconnected(self): # Getter method which returns boolean value which indicates whether thread for client connected to server through sockets has been disconnected or not. 
        
        return self._isDisconnected 
        
    def setIsDisconnected(self, isDisconnected): 
        
        self._isDisconnected = isDisconnected 
        
    def getIsThreadRunning(self): 
        
        return self._isThreadRunning 
        
    def setIsThreadRunning(self, isThreadRunning): 
        
        self._isThreadRunning = isThreadRunning 
        
    def getThread(self): 
        
        return self._thread 
        
    def setThread(self, thread): 
        
        self._thread = thread 
        
class ServerThread: 
    
    def __init__(self): 
        
        self._server = socket.socket() 
        
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        
        self._server.bind(('0.0.0.0', 8080)) 
        
        self._server.listen() 
        
        print('Server started.') 
        
        while True: 
            
            conn, addr = self._server.accept() 
            
            print('Connected with ' + addr[0] + ':' + str(addr[1])) 
            
            clients.append(conn) 
            
            ClientThread(addr[0], addr[1], conn) 

            
ServerThread()

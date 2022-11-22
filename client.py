import socket
import sys
import time
import os
import threading
import random
import string
from PIL import Image


## Global Variables ## 


# Client Variables # 


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 


## Functions ## 

    
def send_message(message): 

    client.send(message) 

        
def send_image(image): 

    client.send(image) 

        
def send_color(color): 

    client.send(color) 

        
def getRandomString(): # Generates a random string of letters and digits and returns the string. Used for generating passwords.  

    lettersAndDigits = string.ascii_letters + string.digits # All letters and digits  

    return ''.join((random.choice(lettersAndDigits) for i in range(20))) # Join method is used to combine a string and an iterable and returns a string.  

    
def getRandomNumber(): # Generates a random number between 1 and 100 and returns the number. Used for generating usernames.  

    return random.randint(1, 100)  

    
def getRandomColor(): # Generates a random color in hex and returns the value. Used for generating colors.  

    return '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  

    
def getRandomImage(): # Generates a random image and returns the image object as bytes object (the image is converted to bytes object before being returned). Used for generating profile pictures (the image is converted to bytes object before being returned).  

    image = Image.new('RGB', (100, 100)) # Create a new black image  

    pixels = image.load() # Create the pixel map  

    for i in range(image.size[0]): # For every pixel:  

        for j in range(image.size[1]):  

            pixels[i, j] = (i, j, 100) # Set the colour accordingly      
            
    return image
            
    return image.tobytes()

    
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

    
class ClientThread: 
    
    def __init__(self): 
        
        self._client = socket.socket() 
        
        self._client.connect(('127.0.0.1', 9999)) 
        
        print('Connected.') 
        
        self._isThreadRunning = True 
        
        self._thread = threading.Thread(target=self.run) 
        
        self._thread.start() 

    def run(self): 

        while self._isThreadRunning: 

            try: 
                def sendMessage(self, message): 

                    self._client.send(message) 


                data = client.recv(1024) 

                if data: 

                    print(data) 

            except: continue  

            
class GUI: 
    
    def __init__(self): 
        
        self._root = tkinter.Tk() 
        
        self._root.title('Client') 
        
        self._root.geometry('300x300') 
        
        self._root.resizable(False, False) 
        
        self._message = tkinter.StringVar() 
        
        self._messageEntry = tkinter.Entry(self._root, textvariable=self._message) 
        
        self._messageEntry.pack(fill=tkinter.X, padx=10, pady=10) 
        
        self._sendButton = tkinter.Button(self._root, text='Send', command=self.sendMessage) 
        
        self._sendButton.pack(fill=tkinter.X, padx=10, pady=10) 
        
        self._messagesFrame = tkinter.Frame(self._root) 
        
        self._messagesFrame.pack() 
        
        self._scrollbar = tkinter.Scrollbar(self._messagesFrame) 
        
        self._scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y) 
        
        self._messages = tkinter.Listbox(self._messagesFrame, height=15, width=50, yscrollcommand=self._scrollbar.set) 
        
        self._messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH) 
        
        self._scrollbar.config(command=self._messages.yview) 
        
        self._clientThread = ClientThread() 
        
        self._root.mainloop() 

    def sendMessage(self): 

        message = self._message.get() 

        self._message.set('') 

        self._clientThread.sendMessage(message) 

        

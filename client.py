import threading
import socket 
import os

## If the user doesn't have tkinter, automatically install it.
try:
    from tkinter import *
except:
    os.system("pip install tkinter")
    from tkinter import *

## Hide the python console.
os.system("title Chat room")
os.system("mode con: cols=1 lines=1")

## Create a GUI for the user to enter their name.
name_root = Tk()
name_root.title("Chat room")
name_root.geometry("200x100")

## Open a socket, connect to the server of the users choice at port 9999.
s = socket.socket()
port = 9999
s.connect(("173.255.232.168", port))
print("Connected to chat server.")

## Create a frame for the name entry box.
name_frame = Frame(name_root)

## Create a label for the name entry box.
name_label = Label(name_frame, text="Please enter your name:")

## Create an entry box for the user to type in their name.
name_entry = Entry(name_frame, width=20)

## Create a send button for the user to send their name.
name_button = Button(name_frame, text="Send", width=10)

## Pack the frames.
name_frame.pack(side=TOP)

## Pack the label and entry box.
name_label.pack(side=TOP)
name_entry.pack(side=TOP)

## Pack the send button.
name_button.pack(side=BOTTOM)

## Create a function to send the name.
def send_name(event=None):
    global name
    name = name_entry.get()
    s.send(name.encode('ascii'))
    name_root.destroy()

## Bind the send button to the send name function.
name_button.bind("<Button-1>", send_name)

## Bind the enter key to the send name function.
name_entry.bind("<Return>", send_name)

## Start the GUI.
name_root.mainloop()

## Create a GUI for the user to interact with.
root = Tk()
root.title("Chat room")
root.geometry("500x500")

## Create a frame for the text box.
text_frame = Frame(root)

## Create a scrollbar for the text box.
scrollbar = Scrollbar(text_frame)

## Create a text box for the user to see the messages.
text_box = Text(text_frame, height=15, width=50, yscrollcommand=scrollbar.set)
text_box.config(state=DISABLED)

## Create a frame for the entry box.
entry_frame = Frame(root)

## Create an entry box for the user to type in.
entry_field = Entry(entry_frame, width=50)

## Create a send button for the user to send messages.
send_button = Button(entry_frame, text="Send", width=10)

## Pack the frames.
text_frame.pack(side=TOP)
entry_frame.pack(side=BOTTOM)

## Pack the text box and scrollbar.
text_box.pack(side=LEFT, fill=Y)
scrollbar.pack(side=RIGHT, fill=Y)

## Pack the entry box and send button.
entry_field.pack(side=LEFT, fill=X, padx=5)
send_button.pack(side=RIGHT)

## Create a function to send messages.
def send(event=None):
    message = entry_field.get()
    entry_field.delete(0, END)
    s.send(message.encode('ascii'))
    text_box.config(state=NORMAL)
    text_box.insert(END, name + ": " + message + "\n")
    text_box.see(END)
    text_box.config(state=DISABLED)

## Bind the send button to the send function.
send_button.bind("<Button-1>", send)

## Bind the enter key to the send function.
entry_field.bind("<Return>", send)

## Create a function to receive messages.
def receive():
    while True:
        try:
            message = s.recv(1024)
            message = message.decode('ascii')
            text_box.config(state=NORMAL)
            text_box.insert(END, message[message.find(":") + 1:] + "\n")
            text_box.see(END)
            text_box.config(state=DISABLED)
        except:
            text_box.config(state=NORMAL)
            text_box.insert(END, "Server is offline.\n")
            text_box.config(state=DISABLED)
            break

## Create a new thread for receiving messages from the server.
threading.Thread(target=receive).start()

## Start the GUI.
root.mainloop()

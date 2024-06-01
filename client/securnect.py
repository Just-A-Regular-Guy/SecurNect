#!/usr/bin/env python3

# Import necessary libraries
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading
import tkinter
import customtkinter
import os
import time
import rsa
from PIL import Image

# Set current directory
current_directory = os.getcwd()

# Loading public and private keys
def load_keys():
    with open('etc/shadow/client_private.pem', 'rb') as f:
        global server_public_key
        server_public_key = rsa.PrivateKey.load_pkcs1(f.read())

    with open('etc/shadow/server_public.pem', 'rb') as f:
        global client_private_key
        client_private_key = rsa.PublicKey.load_pkcs1(f.read())

# Initialize client
load_keys()
print(client_private_key)
print(server_public_key)
client_socket = socket(AF_INET, SOCK_STREAM)
BUFSIZ = 1024

# Initialize username, password, and credentials
username = ''
password = ''
credentials = ''

# Function to handle receiving of messages
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            # Receive message from server
            msg = client_socket.recv(BUFSIZ)
            # Decrypt message
            clear_message = rsa.decrypt(msg, server_public_key).decode()
            print(msg)
            print(clear_message)
            if clear_message == 'PASS':
                # Send credentials to server
                client_socket.send(rsa.encrypt(credentials.encode(), client_private_key))
            else:
                # Display message in chat box
                chat_box.insert(tkinter.END, '{}\n'.format(clear_message))
        except OSError:  # Possibly client has left the chat.
            break

# Function to handle sending of messages
def send(event=None): # event is passed by binder
    """Handles sending of messages."""
    # Get message from input field
    msg = message_entry.get()
    # Encrypt message from input field
    encrypted_message = rsa.encrypt((message_entry.get()).encode(), client_private_key)
    # Clear input field
    message_entry.delete(0, 10000)  # Clears input field.
    # Send message to server
    client_socket.send(encrypted_message)
    if msg == "{quit}":
        # Close client socket and quit GUI
        client_socket.close()
        root.quit()

# Function to handle window closing
#def on_closing(event=None):
#    """This function is to be called when the window is closed."""
#    disconnect()
#    time.sleep(5)  # Wait for 5 seconds to allow the application to close
#    if client_socket.fileno()!= -1:  # Check if the socket is still connected
#        os._exit(0)  # Forcefully terminate the process
#    else:
#        pass
#    root.quit()
#    
#def disconnect():
#    """Handles disconnection from the server."""
#    message_entry.insert(0, "{quit}")  # Tell server we want to exit
#    send()
#    client_socket.close()  # Close the socket
#    print("Disconnected from the server.")
#

# Function to handle window closing
def on_closing(event=None):
    """This function is to be called when the window is closed."""
    print("on_closing() called")
    disconnect()
    print("Disconnecting from server...")
    time.sleep(5)  # Wait for 5 seconds to allow the application to close
    print("Waiting for 5 seconds...")
    if client_socket.fileno()!= -1:  # Check if the socket is still connected
        print("Socket still connected, forcefully terminating process")
        os._exit(0)  # Forcefully terminate the process
    else:
        print("Socket closed, quitting normally")
        pass
    print("Quitting application...")
    root.quit()
    
def disconnect():
    """Handles disconnection from the server."""
    print("disconnect() called")
    message_entry.insert(0, "{quit}")  # Tell server we want to exit
    print("Sending quit message to server...")
    send()
    print("Closing socket...")
    client_socket.close()  # Close the socket
    print("Disconnected from the server.")


# Function to handle login
def login():
    # Get server address and port from input fields
    HOST = server_address_b.get()
    port = server_port_b.get()
    PORT = int(port)

    # Get username and password from input fields
    global UNAME
    global PASSWD
    global credentials

    UNAME = entry_username.get()
    PASSWD = entry_password.get()
    credentials = f'{UNAME}@{PASSWD}'
    print(credentials)

    # Connect to server
    ADDR = (HOST, PORT)
    client_socket.connect(ADDR)

    # Start receive thread
    receive_thread = Thread(target=receive)
    receive_thread.start()

################################################## START OF GUI ##################################################

# GUI global settings
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('800x600')
root.title('Securnect')
root.resizable(width=False, height=False)
#root.iconbitmap(os.path.join(current_directory, 'icon.ico'))
#root.iconbitmap(os.path.join(current_directory,'Python', 'securnect', 'client', 'icon.ico'))

# Create top frame
top_frame = customtkinter.CTkFrame(root, fg_color='#af0000', height=60, corner_radius=0)
top_frame.pack(side=customtkinter.TOP, fill='x')

# Load the image using PIL
image_path = "top.png"
image = Image.open(image_path)

# Create a CTkImage object
ctk_image = customtkinter.CTkImage(light_image=image, dark_image=image, size=(800, 60))

# Create a label and set the image
image_label = customtkinter.CTkLabel(top_frame, image=ctk_image, text="")
image_label.pack(side=customtkinter.TOP)

# Create side frame
side_frame = customtkinter.CTkFrame(root, width=250, height=540, corner_radius=0)
side_frame.pack(side=customtkinter.LEFT, fill='y')

# Create side box
side_box = customtkinter.CTkTextbox(side_frame, width=220, height=510, fg_color='#212121', border_color='#818181', border_width=1, state='disabled',)
side_box.place(relx=0.0558, rely=0.025)

# Create server address input field
server_address_t = customtkinter.CTkLabel(side_box, text='Server address:', text_color='#818181')
server_address_t.place(relx=0.15, rely=0.025)
server_address_b = customtkinter.CTkEntry(side_box, width=165, height=28, fg_color='#404040', border_color='#818181', border_width=1, placeholder_text='Type ipv4 address...')
server_address_b.place(relx=0.12, rely=0.075)

# Create server port input field
server_port_t = customtkinter.CTkLabel(side_box, text='Server port:', text_color='#818181')
server_port_t.place(relx=0.15, rely=0.15)
server_port_b = customtkinter.CTkEntry(side_box, width=165, height=28, fg_color='#404040', border_color='#818181', border_width=1, placeholder_text='Type open port number...')
server_port_b.place(relx=0.12, rely=0.2)

# Create username input field
username_t = customtkinter.CTkLabel(side_box, text='Username:', text_color='#818181')
username_t.place(relx=0.15, rely=0.275)
entry_username = customtkinter.CTkEntry(side_box, width=165, height=28, fg_color='#404040', border_color='#818181', border_width=1, placeholder_text='Type user name...')
entry_username.place(relx=0.12, rely=0.325)

# Create password input field
password_t = customtkinter.CTkLabel(side_box, text='Password:', text_color='#818181')
password_t.place(relx=0.15, rely=0.4)
entry_password = customtkinter.CTkEntry(side_box, width=165, height=28, fg_color='#404040', border_color='#818181', border_width=1, placeholder_text='Type user password...', show='#')
entry_password.place(relx=0.12, rely=0.45)

# Create online users label and text box
online_users_t = customtkinter.CTkLabel(side_box, text='Users online:', text_color='#818181')
online_users_t.place(relx=0.15, rely=0.525)
online_users_b = customtkinter.CTkTextbox(side_box, state='disabled', width=165, height=75, fg_color='#404040', border_color='#818181', border_width=1)
online_users_b.place(relx=0.12, rely=0.575)

# Create client uptime label and text box
client_uptime_t = customtkinter.CTkLabel(side_box, text='Client UpTime:', text_color='#818181')
client_uptime_t.place(relx=0.15, rely=0.745)
client_uptime_b = customtkinter.CTkTextbox(side_box, width=165, height=28, fg_color='#404040', border_color='#818181', border_width=1, text_color='#5BBA6F')
client_uptime_b.place(relx=0.12, rely=0.795)

# Create login button
login_button = customtkinter.CTkButton(side_box, width=140, height=40, text='Login', fg_color='#af0000', bg_color='#212121', font=customtkinter.CTkFont(weight='bold'), command=login)
login_button.place(relx=0.173, rely=0.88)

# Create chat frame
chat_frame = customtkinter.CTkFrame(root, width=550, height=540, fg_color='#313131', corner_radius=0)
chat_frame.pack(fill='both')

# Create chat box
chat_box = customtkinter.CTkTextbox(root, width=520, height=450, fg_color='#313131', bg_color='#313131', border_color='#818181', border_width=1, autoscroll=True)
chat_box.place(relx=0.3315, rely=0.125)

# Create message entry field
message_entry = customtkinter.CTkEntry(root, width=420, height=40, placeholder_text='Type your message here...', fg_color='#404040', bg_color='#313131', border_color='#818181', border_width=1)
message_entry.place(relx=0.3315, rely=0.905)
message_entry.bind("<Return>", command=send)

# Create send button
message_enter = customtkinter.CTkButton(root, width=80, height=40, text='ENTER', fg_color='#af0000', bg_color='#313131', font=customtkinter.CTkFont(weight='bold'), command=send)
message_enter.place(relx=0.881, rely=0.905)

# Function to update uptime
def uptime_update():
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    client_uptime_b.delete('0.0', tkinter.END)
    client_uptime_b.insert('0.0', uptime_str)

# Function to calculate uptime
def uptime():
    start_time = time.time()  # Get the start time
    while True:
        current_time = time.time()  # Get the current time
        global uptime_seconds
        uptime_seconds = int(current_time - start_time)  # Calculate uptime in seconds
        root.after(1000, uptime_update)  # Update GUI every second
        time.sleep(1)  # Wait for 1 second

# Start uptime thread
threading.Thread(target=uptime).start()
root.after(1000, uptime_update)  # Update GUI every second
root.protocol("WM_DELETE_WINDOW", on_closing)

# Starts GUI execution
root.mainloop()

################################################### END OF GUI ###################################################
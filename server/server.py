#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os
import json
import hashlib
import rsa

# Lists For Clients and Their Nicknames
clients = {}
addresses = {}

# Loading public and private keys
def load_keys():
    with open(os.path.join('etc', 'shadow', 'client_public.pem'), 'rb') as f:
        global server_private_key
        server_private_key = rsa.PublicKey.load_pkcs1(f.read())

    with open(os.path.join('etc', 'shadow', 'server_private.pem'), 'rb') as f:
        global client_public_key
        client_public_key = rsa.PrivateKey.load_pkcs1(f.read())
    

# Connection Data
HOST = input('Enter ip adress: ')
PORT = 55555
BUFSIZ = 1024
ADDR = (HOST, PORT)

# Starting Server
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
load_keys()
print(client_public_key)
print(server_private_key)

current_directory = os.getcwd()
# File to store user credentials
CREDENTIALS_FILE = os.path.join(current_directory, 'etc', 'shadow',"user_credentials.json")

def load_credentials():
    """Load user credentials from the file."""
    try:
        with open(CREDENTIALS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_credentials(credentials):
    """Save user credentials to the file."""
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump(credentials, file)

def hash_password(password):
    """Hash the password using SHA-256."""
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

def authenticate(username, password, credentials):
    """Authenticate the user."""
    stored_password = credentials.get(username)
    if stored_password and hash_password(password) == stored_password:
        return True
    return False


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:

        # Load existing credentials
        credentials = load_credentials()
        print(credentials)

        # Accept new connection
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)

        # Request And Store Nickname
        client.send(rsa.encrypt('PASS'.encode(), server_private_key))

        #Print connection information
        print(f'incoming request from:......... {client_address}')        
        # Receive message from client and decode it from UTF-8
        msg = client.recv(BUFSIZ)
        # Decrypt message
        clear_message = rsa.decrypt(msg, client_public_key).decode()
        print(clear_message)
        nickname, password = clear_message.split('@')
        print(nickname)
        print(password)

        if authenticate(nickname, password, credentials):

            # Send public key
            #client.send(public_key))
            # Print And Broadcast Nickname
            print(f'{nickname} has joined the chat room')
            broadcast(f"{nickname} has joined the chat room")
            clients[client] = nickname
            addresses[client] = client_address
            Thread(target=handle_client, args=(client, nickname)).start()

        else :
            print(f"{client_address} authentication failed!")
            client.send(rsa.encrypt("Invalid username or password".encode(), server_private_key),)


def handle_client(client, nickname):
    """Handles a single client connection."""

    name = nickname
    welcome = 'Welcome to the chat room %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(rsa.encrypt(welcome.encode(), server_private_key))
    msg = "server: %s has joined the chat!" % name
    broadcast(msg)
    clients[client] = name

    while True:
        encrypted_msg = client.recv(BUFSIZ)
        msg = rsa.decrypt(encrypted_msg, client_public_key).decode()
        print(encrypted_msg)
        print(msg)
        if msg !=("{quit}"):
            broadcast(msg, name+": ")
        else:
            client.send(rsa.encrypt("{quit}".encode(), server_private_key))
            client.close()
            del clients[client]
            broadcast("%s has left the chat." % name)
            break


def broadcast(msg, prefix=""): # prefix is for name identification
    """Broadcasts a message to all the clients."""

    for sock in clients:
        data = f'{prefix} {msg}'
        sock.send(rsa.encrypt(data.encode(), server_private_key))


def logo():
    print()
    print("||<<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>||")    
    print('||                                                                                                    ||')
    print('||        ███████╗ ███████╗  ██████╗ ██╗   ██╗ ██████╗  ███╗   ██╗ ███████╗  ██████╗ ████████╗        ||')
    print('||        ██╔════╝ ██╔════╝ ██╔════╝ ██║   ██║ ██╔══██╗ ████╗  ██║ ██╔════╝ ██╔════╝ ╚══██╔══╝        ||')
    print('||        ███████╗ █████╗   ██║      ██║   ██║ ██████╔╝ ██╔██╗ ██║ █████╗   ██║         ██║           ||')
    print('||        ╚════██║ ██╔══╝   ██║      ██║   ██║ ██╔══██╗ ██║╚██╗██║ ██╔══╝   ██║         ██║           ||')
    print('||        ███████║ ███████╗ ╚██████╗ ╚██████╔╝ ██║  ██║ ██║ ╚████║ ███████╗ ╚██████╗    ██║           ||')
    print('||        ╚══════╝ ╚══════╝  ╚═════╝  ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚══════╝  ╚═════╝    ╚═╝           ||')
    print('||                                                                                                    ||')
    print("||<<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>><<>>||")
    print() 

# Starting Server
if __name__=="__main__":
    logo()
    SERVER.listen(2) # Listens for 2 connections at max.
    print(f'Waiting for the first connection... Listening on: {HOST}:{PORT}')
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start() # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
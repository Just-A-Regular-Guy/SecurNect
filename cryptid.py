import rsa
import os

# Define the paths
server_public_key_path = os.path.join('etc', 'client_keys', 'server_public.pem')
server_private_key_path = os.path.join('etc', 'shadow', 'server_private.pem')
client_public_key_path = os.path.join('etc', 'shadow', 'client_public.pem')
client_private_key_path = os.path.join('etc', 'client_keys', 'client_private.pem')

# Ensure directories exist
os.makedirs(os.path.dirname(server_public_key_path), exist_ok=True)
os.makedirs(os.path.dirname(server_private_key_path), exist_ok=True)
os.makedirs(os.path.dirname(client_public_key_path), exist_ok=True)
os.makedirs(os.path.dirname(client_private_key_path), exist_ok=True)

# Generate new RSA keys
client_public_key, client_private_key = rsa.newkeys(2048)
server_public_key, server_private_key = rsa.newkeys(2048)

def generate_server_keys():
    with open(server_public_key_path, 'wb') as f:
        f.write(server_public_key.save_pkcs1('PEM'))

    with open(server_private_key_path, 'wb') as f:
        f.write(server_private_key.save_pkcs1('PEM'))

def load_server_keys():
    global server_public_key, server_private_key
    with open(server_public_key_path, 'rb') as f:
        server_public_key = rsa.PublicKey.load_pkcs1(f.read())

    with open(server_private_key_path, 'rb') as f:
        server_private_key = rsa.PrivateKey.load_pkcs1(f.read())

def generate_client_keys():
    with open(client_public_key_path, 'wb') as f:
        f.write(client_public_key.save_pkcs1('PEM'))

    with open(client_private_key_path, 'wb') as f:
        f.write(client_private_key.save_pkcs1('PEM'))

def load_client_keys():
    global client_public_key, client_private_key
    with open(client_public_key_path, 'rb') as f:
        client_public_key = rsa.PublicKey.load_pkcs1(f.read())

    with open(client_private_key_path, 'rb') as f:
        client_private_key = rsa.PrivateKey.load_pkcs1(f.read())

# Generate and save the keys
generate_server_keys()
generate_client_keys()

# Encrypt and decrypt a message
print('|######################|keys check|#######################|')
message = input('Type a message: ')

encrypted_message = rsa.encrypt(message.encode(), server_public_key)
print(f'|###################|Encrypted message|###################|\n{encrypted_message}')

clear_message = rsa.decrypt(encrypted_message, server_private_key).decode()
print(f'|###################|Decrypted message|###################|\n{clear_message}')

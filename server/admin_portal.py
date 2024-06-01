import hashlib
import getpass
import json
import os

current_directory = os.getcwd()
# File to store user credentials
CREDENTIALS_FILE = os.path.join(current_directory, 'etc', 'shadow',"user_credentials.json")
#CREDENTIALS_FILE = os.path.join(current_directory,'server', 'etc', 'shadow',"user_credentials.json")
print(CREDENTIALS_FILE)

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

def create_account(username, password, credentials):
    """Create a new user account."""
    if username not in credentials:
        credentials[username] = hash_password(password)
        save_credentials(credentials)
        print("Account created successfully for {}!".format(username))
    else:
        print("Username {} already exists. Choose another username.".format(username))

def delete_user(json_file, username):
    # Read data from JSON file
    with open(json_file, 'r') as file:
        credentials = json.load(file)

    # Check if the user exists
    if username in credentials:
        # Delete the user
        del credentials[username]
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"User '{username}' not found.")

    # Save the updated data back to the JSON file
    with open(json_file, 'w') as f:
        json.dump(credentials, f, indent=2)


def GOODBYE():
    print('_______________________________________________________________\n')
    print("   ####    #####    #####   #####    ######   ##  ##   #######")
    print('  ##  ##  ##   ##  ##   ##   ## ##    ##  ##  ##  ##    ##')
    print(' ##       ##   ##  ##   ##   ##  ##   ##  ##  ##  ##    ##')
    print(' ##       ##   ##  ##   ##   ##  ##   #####    ####     ####')
    print(' ##  ###  ##   ##  ##   ##   ##  ##   ##  ##    ##      ##')
    print('  ##  ##  ##   ##  ##   ##   ## ##    ##  ##    ##      ##')
    print('   #####   #####    #####   #####    ######    ####    #######')
    print('_______________________________________________________________')

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

user = ()
chat = ()

def core():

    while True:
        choice = input("<>|SECURNECT|<"+user+'>:')

        # Load existing credentials
        credentials = load_credentials()
        json_file_path = os.path.join(current_directory, 'usr', user, "Chat_list.json")

        if choice == 'help' :
            # Commands list
            print()
            print('+-----------------+----------------------------------------+')
            print('|<--------> command list <-------------------------------->|')
            print('+-----------------+----------------------------------------+')
            print('|<> user                                                   |')
            print("|<-------> -ls          show a list of all users           |")
            print("|<-------> -add         create a new user                  |")
            print("|<-------> -rm          delete a user from the user list   |")
            print('+-----------------+----------------------------------------+')
            print('|<> out                                                    |')
            print("|<-------> -l           logout from SECURNECT              |")
            print("|<-------> -e           exit from SECURNECT                |")
            print('+-----------------+----------------------------------------+')
            print('|<> clear               clear all inputs and outputs       |')
            print('+-----------------+----------------------------------------+')
            print()
        elif choice == 'user -ls' :
            # show accounts
            number = 1
            print()
            print('|<----> users  list <---->|')
            print('|<----------------------->|')
            with open(CREDENTIALS_FILE, 'r') as openfile:
                json_object = json.load(openfile)
            for key in json_object.keys():
                print('|')
                print('|<'+ str(number) +'>',key)
                number += 1
            print('|')
            print('|<----------------------->|')
            print()

        elif choice == 'user -add' :
            # Create an account
            username = input('<>|SECURNECT|<>Enter a new username:')
            password = getpass.getpass('<>|SECURNECT|<-------->Enter '+ username +' password:')
            if password == getpass.getpass('<>|SECURNECT|<-------->Enter '+ username +' password:'):
                create_account(username, password, credentials)
            else:
                print('<>|SECURNECT|<>Password mismatch')

            
        elif choice == 'user -rm' : 
            # Delere an account 
            username_to_delete = str(input('<>|SECURNECT|<>Enter a username:'))

            if username_to_delete == 'admin':
                print('you can not delete "admin" user')
            elif username_to_delete == user:
                input('<>|SECURNECT|<>If you proceed, all of your data will be lost and any ongoing activities will be terminated.')
                selection = input('<>|SECURNECT|<>Do you want to delete '+username_to_delete+' ? (y/n) :')

                if selection == 'y':
                    delete_user(CREDENTIALS_FILE, username_to_delete)
                    main()
                elif selection == 'n':
                    print('user '+username_to_delete+' not deleted')
                else: 
                    core()           
            else:
                input('<>|SECURNECT|<>If you proceed, any '+username_to_delete+' data will be lost.')
                selection = input('<>|SECURNECT|<>Do you want to delete '+username_to_delete+' ? (y/n) :')

                if selection == 'y':
                    delete_user(CREDENTIALS_FILE, username_to_delete)
                elif selection == 'n':
                    print('user '+username_to_delete+' not deleted')
                else: 
                    core()

        elif choice == 'out -l' :
            # Logout
            GOODBYE()
            main()
        
        elif choice == 'out -e' :
            # Exit
            GOODBYE()
            break

        elif choice == 'clear' :
            os.system('cls' if os.name == 'nt' else 'clear')
            logo()
            core()

        elif choice == '' :
            core()

        else:
            print("Invalid choice, enter 'help' for more info.")
        
def main():
    """Main function for authentication and account creation."""
    print('\n')
    print('||<-------------------------------------------------------------------------------------------------->||')
    print('||<<>><<>><<>><<>><<>><<>><<>> Welcome to SECURNECT administration system <<>><<>><<>><<>><<>><<>><<>>||')
    print('||<-------------------------------------------------------------------------------------------------->||')
    print('')
    login()

def login():
    
    # Load existing credentials
    credentials = load_credentials()

    log= False
    
    while not log :
            # Log in
            username = input("<>|SECURNECT|<>Enter your username: ")

            if username == '' :
                login()

            else :
                password = getpass.getpass("<>|SECURNECT|<-------->Enter your password: ")
            
                if authenticate(username, password, credentials):
                    print("Authentication successful. Welcome, {}!".format(username))
                    global user
                    user = username
                    log= True
                else:
                    print("Authentication failed. Please check your username and password.")  
    logo()
    core()

if __name__ == "__main__":
    main()

#   ╔══<>|SECURNECT|<>
#   ╚═>    

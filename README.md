# SecurNect

SecurNect is a secure connection management system, currently in its beta version (1.0). The project is in its early stages and primarily intended for testing purposes.

## Project Structure

SecurNect/  
├── client/  
│ ├── etc/shadow/  
│ │ ├── client_private.pem  
│ │ └── server_public.pem  
│ ├── securnect.py  
│ └── top.png  
├── server/  
│ ├── etc/shadow/  
│ │ ├── client_public.pem  
│ │ └── server_private.pem  
│ ├── admin_portal.py  
│ └── server.py  
├── cryptid.py (key generation script)  
├── LICENSE  
└── README.md  

# Getting Started

## Prerequisites

- Python 3.x
- Required Python packages (can be found in `requirements.txt` if available):
   ```bash
   pip install -r requirements.txt
   ```

## Installation  

### Server-Side

1. Clone the repository on the server:
   ```bash
   git clone https://github.com/Just-A-Regular-Guy/SecurNect.git
   cd SecurNect
   ```
   
2. Generate the keys:
   ```bash
   python3 cryptid.py
   ```
  
### Client-Side

1. Clone the repository on the client computers:
   ```bash
   git clone https://github.com/Just-A-Regular-Guy/SecurNect.git
   ```
   
2. Move the keys generated in /server/etc/ on the server, to /client/etc/shadow on the client computers.

## Usage

### Server

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Add some users:
   ```bash
   python3 admin_portal.py
   ```

3. Run the server script:
   ```bash
   python3 server.py
   ```
   
### Client

1. Navigate to the client directory:
   ```bash
   cd client
   ```

3. Run the client script:
   ```bash
   python3 securnect.py
   ```
   
## Credentials

Default credentials for testing:

- Admin: `admin` / `admin`
- User1: `user1` / `pass1`
- User2: `user2` / `pass2`

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

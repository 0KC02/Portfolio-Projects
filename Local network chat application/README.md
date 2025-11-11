# Local Network Chat Application

A simple local network chat application built with Python using Tkinter for the GUI and sockets for network communication.

## Features

- ✅ Multi-user chat support
- ✅ Real-time messaging
- ✅ User authentication with unique usernames
- ✅ User join/leave notifications
- ✅ User count display
- ✅ Timestamped messages
- ✅ Modern and clean GUI
- ✅ Easy server configuration

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)

### Installing Tkinter (if needed)

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

**macOS and Windows:**
Tkinter is usually pre-installed with Python.

## Installation

1. Clone or download this repository
2. No additional packages need to be installed (uses only Python standard library)

## Usage

### Starting the Server

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the server:
```bash
python server.py
```

The server will start on `0.0.0.0:5555` by default, allowing connections from any IP address on your local network.

You should see:
```
Server started on 0.0.0.0:5555
Waiting for clients...
```

### Connecting Clients

1. On the same or different machines on your local network:
   - Open a terminal/command prompt
   - Navigate to the project directory
   - Run the client:
```bash
python client.py
```

2. In the login window:
   - **Server IP**: Enter the IP address of the machine running the server
     - For local testing: `localhost` or `127.0.0.1`
     - For network: Use the server machine's local IP (e.g., `192.168.1.100`)
   - **Port**: Default is `5555` (should match server port)
   - **Username**: Enter a unique username
   - Click **Connect**

3. Once connected, you'll see the chat window where you can:
   - Send messages by typing and pressing Enter or clicking Send
   - See messages from other users
   - View system messages (user joins/leaves)
   - See the current number of connected users

## Finding Your Server IP Address

**Windows:**
```bash
ipconfig
```
Look for IPv4 Address under your network adapter.

**Linux/macOS:**
```bash
ifconfig
```
or
```bash
ip addr show
```
Look for the inet address (not 127.0.0.1).

## Customizing the Server

You can modify the server configuration in `server.py`:

```python
server = ChatServer(host='0.0.0.0', port=5555)
```

- `host='0.0.0.0'` allows connections from any network interface
- `port=5555` is the port number (make sure it's not blocked by firewall)

## Troubleshooting

### Cannot Connect to Server

1. **Check if server is running**: Make sure the server is running and showing "Waiting for clients..."
2. **Check IP address**: Verify you're using the correct server IP address
3. **Check firewall**: Ensure the port (default 5555) is not blocked by firewall
4. **Network connectivity**: Ensure both machines are on the same local network

### Username Already Taken

If you see this error, another user is already using that username. Choose a different username.

### Connection Refused

- Server might not be running
- Wrong IP address or port
- Firewall blocking the connection

## Project Structure

```
.
├── server.py          # Server application (handles clients and messages)
├── client.py          # Client application (GUI chat interface)
├── requirements.txt   # Dependencies (none required)
└── README.md         # This file
```

## How It Works

1. **Server** (`server.py`):
   - Creates a socket server listening on a specified port
   - Accepts multiple client connections using threading
   - Broadcasts messages to all connected clients
   - Manages user list and handles joins/leaves

2. **Client** (`client.py`):
   - Creates a GUI using Tkinter
   - Connects to the server via sockets
   - Sends messages to the server
   - Receives and displays messages from other users
   - Handles login and chat windows

## Future Enhancements

Potential features you could add:
- File sharing
- Emoji support
- Voice chat
- Private messaging between users
- Message history
- Chat rooms/channels
- User avatars

## License

This project is open source and available for educational purposes.

## Notes

- The server must be running before clients can connect
- All communication happens over TCP sockets
- Messages are serialized using JSON
- The application is designed for local network use only


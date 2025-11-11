import socket
import threading
import json
from datetime import datetime

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = {}
        self.lock = threading.Lock()
        
    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server started on {self.host}:{self.port}")
        print("Waiting for clients...")
        
        while True:
            client_socket, address = self.socket.accept()
            print(f"New connection from {address}")
            thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            thread.daemon = True
            thread.start()
    
    def handle_client(self, client_socket, address):
        username = None
        try:
            # Receive username
            data = client_socket.recv(1024).decode('utf-8')
            message = json.loads(data)
            
            if message['type'] == 'login':
                username = message['username']
                
                # Check if username already exists
                with self.lock:
                    if username in [u for u, _ in self.clients.values()]:
                        client_socket.send(json.dumps({
                            'type': 'error',
                            'message': 'Username already taken'
                        }).encode('utf-8'))
                        client_socket.close()
                        return
                    
                    self.clients[address] = (username, client_socket)
                
                # Send successful login
                client_socket.send((json.dumps({
                    'type': 'login_success',
                    'message': f'Welcome to the chat, {username}!'
                }) + '\n').encode('utf-8'))
                
                # Broadcast user joined (to other clients, not the new one)
                self.broadcast({
                    'type': 'user_joined',
                    'username': username,
                    'message': f'{username} joined the chat',
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }, exclude=address)
                
                # Send current user list
                user_list = [u for u, _ in self.clients.values()]
                client_socket.send((json.dumps({
                    'type': 'user_list',
                    'users': user_list
                }) + '\n').encode('utf-8'))
                
                print(f"{username} connected from {address}")
            
            # Handle messages with buffer for partial/incomplete data
            buffer = ""
            while True:
                try:
                    data = client_socket.recv(1024).decode('utf-8')
                    if not data:
                        break
                    
                    buffer += data
                    
                    # Process all complete messages in buffer (newline-delimited)
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if not line:
                            continue
                        
                        try:
                            message = json.loads(line)
                            if message['type'] == 'message':
                                # Broadcast message to all clients (including sender)
                                broadcast_msg = {
                                    'type': 'message',
                                    'username': username,
                                    'message': message['message'],
                                    'timestamp': datetime.now().strftime('%H:%M:%S')
                                }
                                self.broadcast(broadcast_msg)
                                print(f"{username}: {message['message']}")
                            elif message['type'] == 'disconnect':
                                return  # Exit the while loop
                        except json.JSONDecodeError as e:
                            print(f"JSON decode error for {username}: {e}, line: {line[:50]}")
                            continue
                    
                    # If buffer is getting too large, try to parse it anyway (backward compatibility)
                    if len(buffer) > 0 and len(buffer) < 2048:  # Reasonable max size
                        try:
                            message = json.loads(buffer.strip())
                            if message['type'] == 'message':
                                broadcast_msg = {
                                    'type': 'message',
                                    'username': username,
                                    'message': message['message'],
                                    'timestamp': datetime.now().strftime('%H:%M:%S')
                                }
                                self.broadcast(broadcast_msg)
                                print(f"{username}: {message['message']}")
                            elif message['type'] == 'disconnect':
                                return
                            buffer = ""  # Clear buffer after successful parse
                        except json.JSONDecodeError:
                            # Partial message, keep in buffer for next recv
                            pass
                            
                except (ConnectionResetError, ConnectionAbortedError):
                    break
                    
        except (ConnectionResetError, ConnectionAbortedError, json.JSONDecodeError):
            pass
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            # Remove client and broadcast disconnect
            if username:
                with self.lock:
                    if address in self.clients:
                        del self.clients[address]
                
                self.broadcast({
                    'type': 'user_left',
                    'username': username,
                    'message': f'{username} left the chat',
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
                
                print(f"{username} disconnected from {address}")
            
            client_socket.close()
    
    def broadcast(self, message, exclude=None):
        """Broadcast message to all connected clients (optionally excluding sender)"""
        message_json = json.dumps(message)
        disconnected = []
        
        with self.lock:
            for address, (username, client_socket) in self.clients.items():
                if address != exclude:
                    try:
                        # Send message with newline delimiter to help with parsing
                        client_socket.send((message_json + '\n').encode('utf-8'))
                    except:
                        disconnected.append(address)
            
            # Remove disconnected clients
            for address in disconnected:
                if address in self.clients:
                    del self.clients[address]

if __name__ == '__main__':
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Server error: {e}")


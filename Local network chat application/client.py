import socket
import json
import threading
import queue
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from datetime import datetime

class ChatClient:
    def __init__(self):
        self.socket = None
        self.username = None
        self.server_host = 'localhost'
        self.server_port = 5555
        self.connected = False
        self.root = None
        self.message_queue = []  # Queue messages that arrive before chat window is ready
        self.thread_safe_queue = queue.Queue()  # Thread-safe queue for messages from network thread
        
    def create_login_window(self):
        """Create the login window"""
        self.root = tk.Tk()
        self.root.title("Chat Application - Login")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window(self.root, 400, 250)
        
        # Configure style
        self.root.configure(bg='#f0f0f0')
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Local Network Chat",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#333'
        )
        title_label.pack(pady=20)
        
        # Server info frame
        server_frame = tk.Frame(self.root, bg='#f0f0f0')
        server_frame.pack(pady=10)
        
        tk.Label(
            server_frame,
            text="Server IP:",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=5)
        
        self.host_entry = tk.Entry(server_frame, width=20, font=("Arial", 10))
        self.host_entry.insert(0, "localhost")
        self.host_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            server_frame,
            text="Port:",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=5)
        
        self.port_entry = tk.Entry(server_frame, width=10, font=("Arial", 10))
        self.port_entry.insert(0, "5555")
        self.port_entry.pack(side=tk.LEFT, padx=5)
        
        # Username frame
        username_frame = tk.Frame(self.root, bg='#f0f0f0')
        username_frame.pack(pady=10)
        
        tk.Label(
            username_frame,
            text="Username:",
            font=("Arial", 10),
            bg='#f0f0f0'
        ).pack(side=tk.LEFT, padx=5)
        
        self.username_entry = tk.Entry(username_frame, width=25, font=("Arial", 10))
        self.username_entry.pack(side=tk.LEFT, padx=5)
        self.username_entry.focus()
        
        # Bind Enter key to connect
        self.username_entry.bind('<Return>', lambda e: self.connect_to_server())
        self.host_entry.bind('<Return>', lambda e: self.connect_to_server())
        self.port_entry.bind('<Return>', lambda e: self.connect_to_server())
        
        # Connect button
        connect_button = tk.Button(
            self.root,
            text="Connect",
            command=self.connect_to_server,
            bg='#4CAF50',
            fg='white',
            font=("Arial", 11, "bold"),
            padx=20,
            pady=5,
            cursor='hand2'
        )
        connect_button.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Enter your username and click Connect",
            font=("Arial", 9),
            bg='#f0f0f0',
            fg='#666'
        )
        self.status_label.pack()
        
    def connect_to_server(self):
        """Connect to the server"""
        username = self.username_entry.get().strip()
        host = self.host_entry.get().strip()
        
        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
            return
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        try:
            self.status_label.config(text="Connecting...", fg='#666')
            self.root.update()
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.server_host = host
            self.server_port = port
            self.username = username
            self.connected = True
            
            # Send login message
            login_message = json.dumps({
                'type': 'login',
                'username': username
            })
            self.socket.send(login_message.encode('utf-8'))
            
            # Wait for login response (with timeout) before starting listener thread
            self.socket.settimeout(3)
            try:
                response = self.socket.recv(1024).decode('utf-8')
                # Remove newline delimiter if present
                response = response.strip()
                message = json.loads(response)
                
                if message['type'] == 'error':
                    self.status_label.config(text=message['message'], fg='red')
                    self.socket.close()
                    self.connected = False
                    return
                elif message['type'] == 'login_success':
                    # Reset timeout to None (blocking mode) for normal operation
                    self.socket.settimeout(None)
                    # Start listening thread after successful login
                    listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
                    listen_thread.start()
                    self.root.after(100, self.create_chat_window)
            except socket.timeout:
                # Timeout waiting for login response - connection might be okay
                # But this shouldn't normally happen, so close connection
                self.status_label.config(text="Login timeout - connection failed", fg='red')
                self.socket.close()
                self.connected = False
                messagebox.showerror("Connection Error", "Failed to receive login response from server.")
            except json.JSONDecodeError:
                # If we got a response but couldn't decode it, it might be okay
                # Reset timeout and proceed (the response might have been consumed by listener)
                self.socket.settimeout(None)
                listen_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
                listen_thread.start()
                self.root.after(100, self.create_chat_window)
                
        except ConnectionRefusedError:
            self.status_label.config(text="Connection refused. Is the server running?", fg='red')
            messagebox.showerror("Connection Error", "Could not connect to server.\nMake sure the server is running.")
            if self.socket:
                self.socket.close()
            self.connected = False
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg='red')
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
            if self.socket:
                self.socket.close()
            self.connected = False
    
    def create_chat_window(self):
        """Create the chat window"""
        self.root.destroy()
        
        self.root = tk.Tk()
        self.root.title(f"Chat - {self.username}")
        self.root.geometry("800x600")
        
        # Center window
        self.center_window(self.root, 800, 600)
        
        # Configure style
        self.root.configure(bg='#f0f0f0')
        
        # Top frame with user info
        top_frame = tk.Frame(self.root, bg='#2c3e50', height=40)
        top_frame.pack(fill=tk.X)
        top_frame.pack_propagate(False)
        
        user_label = tk.Label(
            top_frame,
            text=f"Logged in as: {self.username} | Server: {self.server_host}:{self.server_port}",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='white'
        )
        user_label.pack(side=tk.LEFT, padx=10, pady=8)
        
        # Users online label
        self.users_label = tk.Label(
            top_frame,
            text="Users: 1",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#3498db'
        )
        self.users_label.pack(side=tk.RIGHT, padx=10, pady=8)
        
        # Main frame with chat and user list
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Chat area frame
        chat_frame = tk.Frame(main_frame, bg='#f0f0f0')
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Arial", 10),
            bg='white',
            fg='#333',
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for styling - ensure colors are visible
        self.chat_display.tag_config('system', foreground='#7f8c8d', font=("Arial", 9, "italic"))
        self.chat_display.tag_config('message', foreground='#000000', font=("Arial", 10))  # Black for visibility
        self.chat_display.tag_config('username', foreground='#0000FF', font=("Arial", 10, "bold"))  # Blue for visibility
        
        # Ensure default text color is visible (black on white)
        self.chat_display.config(fg='#000000', bg='white', insertbackground='#000000')
        
        # User list frame (optional, can be expanded later)
        # For now, we'll just show the count in the top frame
        
        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg='white',
            fg='#333'
        )
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        self.message_entry.focus()
        
        send_button = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg='#3498db',
            fg='white',
            font=("Arial", 11, "bold"),
            padx=20,
            cursor='hand2'
        )
        send_button.pack(side=tk.RIGHT)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Display welcome message
        self.display_system_message("Welcome to the chat!")
        
        # Process any queued messages that arrived before window was ready
        if self.message_queue:
            for queued_msg in self.message_queue:
                self.handle_message(queued_msg)
            self.message_queue = []
        
        # Start polling the thread-safe queue for incoming messages
        self.process_message_queue()
    
    def send_message(self):
        """Send a message to the server"""
        message = self.message_entry.get().strip()
        if not message or not self.connected:
            return
        
        try:
            message_json = json.dumps({
                'type': 'message',
                'message': message
            })
            # Send with newline delimiter for consistency with server
            self.socket.send((message_json + '\n').encode('utf-8'))
            self.message_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
            self.connected = False
    
    def process_message_queue(self):
        """Process messages from the thread-safe queue (called from main thread)"""
        try:
            while True:
                try:
                    # Get message from queue (non-blocking)
                    message = self.thread_safe_queue.get_nowait()
                    # Process the message on the main thread
                    self.handle_message(message)
                except queue.Empty:
                    # No more messages
                    break
        except Exception as e:
            print(f"Error processing message queue: {e}")
        
        # Schedule next check in 100ms if connected
        if self.connected and hasattr(self, 'root') and self.root:
            try:
                self.root.after(100, self.process_message_queue)
            except (RuntimeError, tk.TclError):
                # Main loop stopped or window destroyed
                pass
    
    def safe_gui_call(self, func, *args):
        """Safely queue a GUI function call from a thread"""
        try:
            # For handle_message, put it in the thread-safe queue instead of using root.after()
            if func == self.handle_message and args:
                self.thread_safe_queue.put(args[0])  # Put the message dict in queue
            else:
                # For other functions, try to use root.after() but catch errors
                if hasattr(self, 'root') and self.root:
                    try:
                        if self.root.winfo_exists():
                            self.root.after(0, lambda: func(*args))
                    except (tk.TclError, RuntimeError):
                        pass
        except Exception as e:
            print(f"Error in safe_gui_call: {e}")
    
    def listen_for_messages(self):
        """Listen for messages from the server"""
        buffer = ""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                # Add to buffer (handle partial messages and multiple messages)
                buffer += data
                
                # Process all complete JSON messages in the buffer
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        message = json.loads(line)
                        self.safe_gui_call(self.handle_message, message)
                    except json.JSONDecodeError as e:
                        # Skip malformed JSON
                        continue
                
                # Handle case where buffer might contain a complete JSON without newline
                # (backward compatibility for messages without delimiter)
                if buffer.strip() and len(buffer) > 0:
                    try:
                        # Try to parse as complete JSON
                        message = json.loads(buffer.strip())
                        self.safe_gui_call(self.handle_message, message)
                        buffer = ""
                    except json.JSONDecodeError:
                        # Partial message, keep in buffer for next recv
                        pass
                
            except (ConnectionResetError, ConnectionAbortedError):
                if self.connected:
                    self.safe_gui_call(self.handle_disconnect)
                break
            except socket.timeout:
                # Socket timeout - this shouldn't happen in blocking mode
                # but handle it gracefully by continuing to listen
                continue
            except Exception as e:
                if self.connected:
                    # Only print unexpected errors, ignore timeouts and GUI errors silently
                    error_msg = str(e).lower()
                    if "timeout" not in error_msg and "main loop" not in error_msg:
                        print(f"Error receiving message: {e}")
                    # For timeout or GUI errors, just continue listening
                    if "timeout" in error_msg or "main loop" in error_msg:
                        continue
                break
    
    def handle_message(self, message):
        """Handle incoming messages"""
        msg_type = message.get('type')
        
        if msg_type == 'message':
            username = message.get('username', 'Unknown')
            text = message.get('message', '')
            timestamp = message.get('timestamp', '')
            
            # Only display if chat window is ready, otherwise queue it
            if hasattr(self, 'chat_display') and self.chat_display:
                try:
                    self.display_message(username, text, timestamp)
                except Exception as e:
                    print(f"Error displaying message: {e}")
            else:
                # Queue message for later display
                self.message_queue.append(message)
        
        elif msg_type == 'user_joined':
            if hasattr(self, 'chat_display'):
                self.display_system_message(message.get('message', ''))
            if 'users' in message and hasattr(self, 'users_label'):
                self.update_user_count(message['users'])
        
        elif msg_type == 'user_left':
            if hasattr(self, 'chat_display'):
                self.display_system_message(message.get('message', ''))
        
        elif msg_type == 'user_list':
            users = message.get('users', [])
            if hasattr(self, 'users_label'):
                self.update_user_count(users)
    
    def display_message(self, username, message, timestamp):
        """Display a chat message"""
        if not hasattr(self, 'chat_display') or not self.chat_display:
            return
            
        try:
            # Enable editing
            self.chat_display.config(state=tk.NORMAL)
            
            # Insert message parts with tags for styling
            start_pos = self.chat_display.index(tk.END)
            self.chat_display.insert(tk.END, f"[{timestamp}] ", 'system')
            self.chat_display.insert(tk.END, f"{username}: ", 'username')
            self.chat_display.insert(tk.END, f"{message}\n", 'message')
            
            # Disable editing
            self.chat_display.config(state=tk.DISABLED)
            
            # Scroll to end to show the latest message
            self.chat_display.see(tk.END)
            
            # Force immediate update of the display
            self.chat_display.update_idletasks()
            
        except tk.TclError:
            # Widget destroyed - ignore silently
            pass
        except Exception as e:
            print(f"Error in display_message: {e}")
    
    def display_system_message(self, message):
        """Display a system message"""
        if not hasattr(self, 'chat_display'):
            return
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"{message}\n", 'system')
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def update_user_count(self, users):
        """Update the user count display"""
        if not hasattr(self, 'users_label'):
            return
        count = len(users)
        self.users_label.config(text=f"Users: {count}")
    
    def handle_disconnect(self):
        """Handle disconnection from server"""
        self.connected = False
        messagebox.showwarning("Disconnected", "Connection to server lost.")
        self.root.destroy()
    
    def on_closing(self):
        """Handle window close event"""
        if self.connected:
            try:
                disconnect_message = json.dumps({'type': 'disconnect'})
                self.socket.send(disconnect_message.encode('utf-8'))
                self.socket.close()
            except:
                pass
        self.root.destroy()
    
    def center_window(self, window, width, height):
        """Center the window on screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    def run(self):
        """Start the client application"""
        self.create_login_window()
        self.root.mainloop()

if __name__ == '__main__':
    client = ChatClient()
    client.run()


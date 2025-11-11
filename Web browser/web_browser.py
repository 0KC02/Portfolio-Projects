#!/usr/bin/env python3
"""
Advanced Web Browser built with Python and Tkinter
Features: Tabbed browsing, bookmarks, history, downloads, and more
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import requests
from urllib.parse import urlparse, urljoin
import webbrowser
import os
import json
import threading
import time
from datetime import datetime
import re
from bs4 import BeautifulSoup
import io
from PIL import Image, ImageTk

class WebBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Web Browser")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Browser data
        self.bookmarks = self.load_bookmarks()
        self.history = self.load_history()
        self.downloads = []
        self.current_tab = None
        self.tabs = []
        
        # Create GUI
        self.create_menu()
        self.create_toolbar()
        self.create_notebook()
        self.create_status_bar()
        
        # Create first tab
        self.new_tab()
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_menu(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Tab", command=self.new_tab, accelerator="Ctrl+T")
        file_menu.add_command(label="New Window", command=self.new_window, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Open File", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save Page As...", command=self.save_page, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Reload", command=self.reload_page, accelerator="F5")
        view_menu.add_command(label="Stop", command=self.stop_loading, accelerator="Esc")
        view_menu.add_separator()
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom, accelerator="Ctrl+0")
        
        # Bookmarks menu
        bookmarks_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bookmarks", menu=bookmarks_menu)
        bookmarks_menu.add_command(label="Add Bookmark", command=self.add_bookmark, accelerator="Ctrl+D")
        bookmarks_menu.add_command(label="Bookmark Manager", command=self.bookmark_manager)
        bookmarks_menu.add_separator()
        self.populate_bookmarks_menu(bookmarks_menu)
        
        # History menu
        history_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="History", menu=history_menu)
        history_menu.add_command(label="Show History", command=self.show_history)
        history_menu.add_command(label="Clear History", command=self.clear_history)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Downloads", command=self.show_downloads)
        tools_menu.add_command(label="Settings", command=self.show_settings)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-t>', lambda e: self.new_tab())
        self.root.bind('<Control-n>', lambda e: self.new_window())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_page())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-d>', lambda e: self.add_bookmark())
        self.root.bind('<F5>', lambda e: self.reload_page())
        self.root.bind('<Escape>', lambda e: self.stop_loading())
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())
        self.root.bind('<Control-f>', lambda e: self.find_text())
    
    def create_toolbar(self):
        """Create the navigation toolbar"""
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Navigation buttons
        self.back_btn = ttk.Button(toolbar_frame, text="←", command=self.go_back, width=3)
        self.back_btn.grid(row=0, column=0, padx=2)
        
        self.forward_btn = ttk.Button(toolbar_frame, text="→", command=self.go_forward, width=3)
        self.forward_btn.grid(row=0, column=1, padx=2)
        
        self.reload_btn = ttk.Button(toolbar_frame, text="↻", command=self.reload_page, width=3)
        self.reload_btn.grid(row=0, column=2, padx=2)
        
        self.home_btn = ttk.Button(toolbar_frame, text="🏠", command=self.go_home, width=3)
        self.home_btn.grid(row=0, column=3, padx=2)
        
        # Address bar
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(toolbar_frame, textvariable=self.url_var, font=("Arial", 10))
        self.url_entry.grid(row=0, column=4, sticky="ew", padx=5)
        self.url_entry.bind('<Return>', self.navigate_to_url)
        
        # Go button
        self.go_btn = ttk.Button(toolbar_frame, text="Go", command=self.navigate_to_url)
        self.go_btn.grid(row=0, column=5, padx=2)
        
        # Bookmark button
        self.bookmark_btn = ttk.Button(toolbar_frame, text="★", command=self.add_bookmark, width=3)
        self.bookmark_btn.grid(row=0, column=6, padx=2)
        
        # Configure grid weights
        toolbar_frame.grid_columnconfigure(4, weight=1)
    
    def create_notebook(self):
        """Create the tabbed interface"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        # Add close button to tabs
        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[12, 8])
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var)
        self.status_label.grid(row=0, column=0, sticky="w")
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var, length=200)
        self.progress_bar.grid(row=0, column=1, sticky="e", padx=10)
    
    def new_tab(self, url="about:blank"):
        """Create a new browser tab"""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text="New Tab")
        
        # Create text widget for content display
        text_widget = tk.Text(tab_frame, wrap=tk.WORD, state=tk.DISABLED, 
                            font=("Arial", 10), bg="white", fg="black")
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        # Tab data
        tab_data = {
            'frame': tab_frame,
            'text_widget': text_widget,
            'url': url,
            'title': "New Tab",
            'history': [],
            'history_index': -1,
            'can_go_back': False,
            'can_go_forward': False
        }
        
        self.tabs.append(tab_data)
        self.notebook.select(tab_frame)
        self.current_tab = tab_data
        
        if url != "about:blank":
            self.navigate_to_url_in_tab(tab_data, url)
    
    def on_tab_change(self, event):
        """Handle tab change events"""
        selected_tab = self.notebook.select()
        if selected_tab:
            tab_frame = self.notebook.nametowidget(selected_tab)
            for tab in self.tabs:
                if tab['frame'] == tab_frame:
                    self.current_tab = tab
                    self.update_navigation_buttons()
                    self.url_var.set(tab['url'])
                    break
    
    def navigate_to_url(self, event=None):
        """Navigate to URL entered in address bar"""
        if self.current_tab:
            url = self.url_var.get().strip()
            self.navigate_to_url_in_tab(self.current_tab, url)
    
    def navigate_to_url_in_tab(self, tab, url):
        """Navigate to URL in specific tab"""
        if not url:
            return
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://', 'file://', 'about:')):
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                # Treat as search query
                url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
        
        # Update status
        self.status_var.set("Loading...")
        self.progress_var.set(0)
        
        # Start loading in thread
        thread = threading.Thread(target=self.load_url, args=(tab, url))
        thread.daemon = True
        thread.start()
    
    def load_url(self, tab, url):
        """Load URL content in a separate thread"""
        try:
            # Update progress
            self.root.after(0, lambda: self.progress_var.set(20))
            
            # Handle special URLs
            if url.startswith('about:'):
                self.root.after(0, lambda: self.display_about_page(tab))
                return
            
            # Make request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            self.root.after(0, lambda: self.progress_var.set(40))
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            self.root.after(0, lambda: self.progress_var.set(70))
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else url
            
            # Remove scripts and styles
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text_content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Update UI in main thread
            self.root.after(0, lambda: self.update_tab_content(tab, url, title_text, text_content))
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error loading {url}: {str(e)}"
            self.root.after(0, lambda: self.display_error(tab, error_msg))
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.root.after(0, lambda: self.display_error(tab, error_msg))
    
    def update_tab_content(self, tab, url, title, content):
        """Update tab content in main thread"""
        # Update tab data
        tab['url'] = url
        tab['title'] = title
        
        # Add to history
        if not tab['history'] or tab['history'][-1] != url:
            tab['history'].append(url)
            tab['history_index'] = len(tab['history']) - 1
        
        # Update tab title
        self.notebook.tab(tab['frame'], text=title[:20] + "..." if len(title) > 20 else title)
        
        # Update address bar
        self.url_var.set(url)
        
        # Update content
        tab['text_widget'].config(state=tk.NORMAL)
        tab['text_widget'].delete(1.0, tk.END)
        tab['text_widget'].insert(1.0, content)
        tab['text_widget'].config(state=tk.DISABLED)
        
        # Update navigation buttons
        self.update_navigation_buttons()
        
        # Update status
        self.status_var.set(f"Loaded: {title}")
        self.progress_var.set(100)
        
        # Add to global history
        self.add_to_history(url, title)
    
    def display_about_page(self, tab):
        """Display about page"""
        about_content = """
        Python Web Browser
        ==================
        
        Welcome to the Python Web Browser!
        
        Features:
        • Tabbed browsing
        • Bookmarks
        • History
        • Downloads
        • Search functionality
        • Modern interface
        
        Built with Python, Tkinter, and Requests.
        
        Version: 1.0.0
        """
        
        tab['url'] = "about:blank"
        tab['title'] = "About"
        self.notebook.tab(tab['frame'], text="About")
        self.url_var.set("about:blank")
        
        tab['text_widget'].config(state=tk.NORMAL)
        tab['text_widget'].delete(1.0, tk.END)
        tab['text_widget'].insert(1.0, about_content)
        tab['text_widget'].config(state=tk.DISABLED)
        
        self.status_var.set("Ready")
        self.progress_var.set(100)
    
    def display_error(self, tab, error_msg):
        """Display error message"""
        tab['text_widget'].config(state=tk.NORMAL)
        tab['text_widget'].delete(1.0, tk.END)
        tab['text_widget'].insert(1.0, f"Error: {error_msg}")
        tab['text_widget'].config(state=tk.DISABLED)
        
        self.status_var.set("Error")
        self.progress_var.set(0)
    
    def update_navigation_buttons(self):
        """Update navigation button states"""
        if self.current_tab:
            self.back_btn.config(state=tk.NORMAL if self.current_tab['can_go_back'] else tk.DISABLED)
            self.forward_btn.config(state=tk.NORMAL if self.current_tab['can_go_forward'] else tk.DISABLED)
    
    def go_back(self):
        """Go back in history"""
        if self.current_tab and self.current_tab['can_go_back']:
            if self.current_tab['history_index'] > 0:
                self.current_tab['history_index'] -= 1
                url = self.current_tab['history'][self.current_tab['history_index']]
                self.navigate_to_url_in_tab(self.current_tab, url)
    
    def go_forward(self):
        """Go forward in history"""
        if self.current_tab and self.current_tab['can_go_forward']:
            if self.current_tab['history_index'] < len(self.current_tab['history']) - 1:
                self.current_tab['history_index'] += 1
                url = self.current_tab['history'][self.current_tab['history_index']]
                self.navigate_to_url_in_tab(self.current_tab, url)
    
    def reload_page(self):
        """Reload current page"""
        if self.current_tab and self.current_tab['url']:
            self.navigate_to_url_in_tab(self.current_tab, self.current_tab['url'])
    
    def go_home(self):
        """Go to home page"""
        self.navigate_to_url_in_tab(self.current_tab, "https://www.google.com")
    
    def stop_loading(self):
        """Stop loading current page"""
        self.status_var.set("Stopped")
        self.progress_var.set(0)
    
    def new_window(self):
        """Open new browser window"""
        new_root = tk.Toplevel(self.root)
        WebBrowser(new_root)
    
    def open_file(self):
        """Open local HTML file"""
        file_path = filedialog.askopenfilename(
            title="Open HTML File",
            filetypes=[("HTML files", "*.html *.htm"), ("All files", "*.*")]
        )
        if file_path:
            self.navigate_to_url_in_tab(self.current_tab, f"file://{file_path}")
    
    def save_page(self):
        """Save current page"""
        if self.current_tab and self.current_tab['url']:
            file_path = filedialog.asksaveasfilename(
                title="Save Page As",
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    content = self.current_tab['text_widget'].get(1.0, tk.END)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    messagebox.showinfo("Success", f"Page saved to {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def add_bookmark(self):
        """Add current page to bookmarks"""
        if self.current_tab and self.current_tab['url'] and self.current_tab['url'] != "about:blank":
            title = self.current_tab['title']
            url = self.current_tab['url']
            
            bookmark = {
                'title': title,
                'url': url,
                'date_added': datetime.now().isoformat()
            }
            
            self.bookmarks.append(bookmark)
            self.save_bookmarks()
            messagebox.showinfo("Bookmark Added", f"Added '{title}' to bookmarks")
        else:
            messagebox.showwarning("No Page", "No page to bookmark")
    
    def bookmark_manager(self):
        """Open bookmark manager"""
        manager_window = tk.Toplevel(self.root)
        manager_window.title("Bookmark Manager")
        manager_window.geometry("600x400")
        
        # Create treeview for bookmarks
        tree_frame = ttk.Frame(manager_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('URL', 'Date'), show='tree headings')
        tree.heading('#0', text='Title')
        tree.heading('URL', text='URL')
        tree.heading('Date', text='Date Added')
        
        tree.column('#0', width=200)
        tree.column('URL', width=300)
        tree.column('Date', width=150)
        
        # Add bookmarks to tree
        for i, bookmark in enumerate(self.bookmarks):
            tree.insert('', 'end', text=bookmark['title'], 
                       values=(bookmark['url'], bookmark['date_added']))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(manager_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Open", 
                  command=lambda: self.open_bookmark(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete", 
                  command=lambda: self.delete_bookmark(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", 
                  command=manager_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def open_bookmark(self, tree):
        """Open selected bookmark"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            url = item['values'][0]
            self.navigate_to_url_in_tab(self.current_tab, url)
    
    def delete_bookmark(self, tree):
        """Delete selected bookmark"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            title = item['text']
            
            # Remove from bookmarks list
            self.bookmarks = [b for b in self.bookmarks if b['title'] != title]
            self.save_bookmarks()
            
            # Remove from tree
            tree.delete(selection[0])
    
    def populate_bookmarks_menu(self, menu):
        """Populate bookmarks menu"""
        for bookmark in self.bookmarks[-10:]:  # Show last 10 bookmarks
            menu.add_command(label=bookmark['title'][:30] + "...", 
                           command=lambda url=bookmark['url']: 
                           self.navigate_to_url_in_tab(self.current_tab, url))
    
    def add_to_history(self, url, title):
        """Add page to history"""
        history_item = {
            'url': url,
            'title': title,
            'timestamp': datetime.now().isoformat()
        }
        self.history.append(history_item)
        self.save_history()
    
    def show_history(self):
        """Show browsing history"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Browsing History")
        history_window.geometry("700x500")
        
        # Create treeview for history
        tree_frame = ttk.Frame(history_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('URL', 'Time'), show='tree headings')
        tree.heading('#0', text='Title')
        tree.heading('URL', text='URL')
        tree.heading('Time', text='Time')
        
        tree.column('#0', width=250)
        tree.column('URL', width=300)
        tree.column('Time', width=150)
        
        # Add history items to tree (most recent first)
        for item in reversed(self.history[-100:]):  # Show last 100 items
            time_str = datetime.fromisoformat(item['timestamp']).strftime('%Y-%m-%d %H:%M')
            tree.insert('', 'end', text=item['title'], 
                       values=(item['url'], time_str))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(history_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Open", 
                  command=lambda: self.open_history_item(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear History", 
                  command=lambda: self.clear_history_confirm(history_window)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", 
                  command=history_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def open_history_item(self, tree):
        """Open selected history item"""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            url = item['values'][0]
            self.navigate_to_url_in_tab(self.current_tab, url)
    
    def clear_history_confirm(self, parent):
        """Confirm and clear history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear all browsing history?"):
            self.clear_history()
            parent.destroy()
    
    def clear_history(self):
        """Clear browsing history"""
        self.history = []
        self.save_history()
        messagebox.showinfo("History Cleared", "Browsing history has been cleared")
    
    def show_downloads(self):
        """Show downloads window"""
        downloads_window = tk.Toplevel(self.root)
        downloads_window.title("Downloads")
        downloads_window.geometry("600x300")
        
        # Create treeview for downloads
        tree_frame = ttk.Frame(downloads_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=('Status', 'Size'), show='tree headings')
        tree.heading('#0', text='File')
        tree.heading('Status', text='Status')
        tree.heading('Size', text='Size')
        
        tree.column('#0', width=300)
        tree.column('Status', width=100)
        tree.column('Size', width=100)
        
        # Add downloads to tree
        for download in self.downloads:
            tree.insert('', 'end', text=download['filename'], 
                       values=(download['status'], download['size']))
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(downloads_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="Open Folder", 
                  command=self.open_downloads_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear List", 
                  command=lambda: self.clear_downloads(tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Close", 
                  command=downloads_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def open_downloads_folder(self):
        """Open downloads folder"""
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        if os.path.exists(downloads_path):
            os.startfile(downloads_path)
        else:
            messagebox.showwarning("Downloads Folder", "Downloads folder not found")
    
    def clear_downloads(self, tree):
        """Clear downloads list"""
        self.downloads = []
        for item in tree.get_children():
            tree.delete(item)
    
    def show_settings(self):
        """Show settings window"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        
        # Settings content
        ttk.Label(settings_window, text="Browser Settings", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Home page setting
        home_frame = ttk.Frame(settings_window)
        home_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(home_frame, text="Home Page:").pack(side=tk.LEFT)
        home_var = tk.StringVar(value="https://www.google.com")
        home_entry = ttk.Entry(home_frame, textvariable=home_var, width=30)
        home_entry.pack(side=tk.RIGHT, padx=10)
        
        # Search engine setting
        search_frame = ttk.Frame(settings_window)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(search_frame, text="Search Engine:").pack(side=tk.LEFT)
        search_var = tk.StringVar(value="Google")
        search_combo = ttk.Combobox(search_frame, textvariable=search_var, 
                                   values=["Google", "Bing", "DuckDuckGo"], width=27)
        search_combo.pack(side=tk.RIGHT, padx=10)
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        ttk.Button(button_frame, text="Save", 
                  command=lambda: self.save_settings(home_var.get(), search_var.get())).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=settings_window.destroy).pack(side=tk.RIGHT, padx=5)
    
    def save_settings(self, home_page, search_engine):
        """Save browser settings"""
        settings = {
            'home_page': home_page,
            'search_engine': search_engine
        }
        
        try:
            with open('browser_settings.json', 'w') as f:
                json.dump(settings, f)
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        Python Web Browser v1.0.0
        
        A modern web browser built with Python and Tkinter.
        
        Features:
        • Tabbed browsing
        • Bookmarks management
        • Browsing history
        • Downloads tracking
        • Search functionality
        • Modern interface
        
        Built with:
        • Python 3.x
        • Tkinter (GUI)
        • Requests (HTTP)
        • BeautifulSoup (HTML parsing)
        
        © 2024 Python Web Browser
        """
        
        messagebox.showinfo("About Python Web Browser", about_text)
    
    def cut_text(self):
        """Cut selected text"""
        if self.current_tab:
            self.current_tab['text_widget'].event_generate("<<Cut>>")
    
    def copy_text(self):
        """Copy selected text"""
        if self.current_tab:
            self.current_tab['text_widget'].event_generate("<<Copy>>")
    
    def paste_text(self):
        """Paste text"""
        if self.current_tab:
            self.current_tab['text_widget'].event_generate("<<Paste>>")
    
    def find_text(self):
        """Open find dialog"""
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("300x100")
        find_window.transient(self.root)
        find_window.grab_set()
        
        ttk.Label(find_window, text="Find:").pack(pady=5)
        
        find_var = tk.StringVar()
        find_entry = ttk.Entry(find_window, textvariable=find_var, width=30)
        find_entry.pack(pady=5)
        find_entry.focus()
        
        def do_find():
            if self.current_tab:
                text_widget = self.current_tab['text_widget']
                search_text = find_var.get()
                if search_text:
                    # Simple text search
                    content = text_widget.get(1.0, tk.END)
                    if search_text.lower() in content.lower():
                        messagebox.showinfo("Find", f"Found '{search_text}'")
                    else:
                        messagebox.showinfo("Find", f"'{search_text}' not found")
        
        ttk.Button(find_window, text="Find", command=do_find).pack(pady=5)
        find_entry.bind('<Return>', lambda e: do_find())
    
    def zoom_in(self):
        """Zoom in on content"""
        if self.current_tab:
            current_font = self.current_tab['text_widget']['font']
            if isinstance(current_font, tuple):
                font_family, font_size = current_font[0], int(current_font[1])
            else:
                font_family, font_size = "Arial", 10
            
            new_size = min(font_size + 2, 24)
            self.current_tab['text_widget'].config(font=(font_family, new_size))
    
    def zoom_out(self):
        """Zoom out on content"""
        if self.current_tab:
            current_font = self.current_tab['text_widget']['font']
            if isinstance(current_font, tuple):
                font_family, font_size = current_font[0], int(current_font[1])
            else:
                font_family, font_size = "Arial", 10
            
            new_size = max(font_size - 2, 8)
            self.current_tab['text_widget'].config(font=(font_family, new_size))
    
    def reset_zoom(self):
        """Reset zoom to default"""
        if self.current_tab:
            self.current_tab['text_widget'].config(font=("Arial", 10))
    
    def load_bookmarks(self):
        """Load bookmarks from file"""
        try:
            with open('bookmarks.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception:
            return []
    
    def save_bookmarks(self):
        """Save bookmarks to file"""
        try:
            with open('bookmarks.json', 'w') as f:
                json.dump(self.bookmarks, f, indent=2)
        except Exception as e:
            print(f"Error saving bookmarks: {e}")
    
    def load_history(self):
        """Load history from file"""
        try:
            with open('history.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception:
            return []

    def save_history(self):
        """Save history to file"""
        try:
            with open('history.json', 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

def main():
    """Main function to run the browser"""
    root = tk.Tk()
    browser = WebBrowser(root)
    
    # Set window icon (if available)
    try:
        root.iconbitmap('browser_icon.ico')
    except:
        pass
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
